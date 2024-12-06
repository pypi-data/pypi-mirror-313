from abc import ABCMeta
from dataclasses import dataclass, replace
from typing import Callable, Hashable, Iterable, Iterator, Optional, Set, Tuple, Union

from tdm.abstract.datamodel import AbstractDomain, AbstractFact, AbstractLinkFact, EnsureIdentifiable, FactStatus, Identifiable
from tdm.abstract.datamodel.duplicatable import Duplicatable
from tdm.abstract.datamodel.fact import AbstractValueFact
from tdm.abstract.datamodel.value import AbstractValue
from tdm.abstract.json_schema import generate_model
from tdm.datamodel.common import PrunableMixin, ViewContainer
from tdm.datamodel.domain import AtomValueType, ComponentValueType, CompositeValueType


@generate_model(label='atom')
@dataclass(frozen=True)
class AtomValueFact(Identifiable, AbstractValueFact[AtomValueType, AbstractValue], PrunableMixin):
    """
    Represents a fact that holds an atomic value.

    If the fact status is FactStatus.NEW `value` should be a tuple.
    If the fact status is FactStatus.APPROVED `value` should be single-valued.
    """

    def replace_with_domain(self, domain: AbstractDomain) -> 'AtomValueFact':
        if isinstance(self.type_id, str):
            domain_type = domain.get_type(self.type_id)
            if not isinstance(domain_type, AtomValueType):
                raise ValueError
            return replace(self, type_id=domain_type)
        return self

    def _as_tuple(self) -> tuple:
        return self.id, self.str_type_id, self.value

    def __eq__(self, other):
        if not isinstance(other, AtomValueFact):
            return NotImplemented
        return self._as_tuple() == other._as_tuple()

    def __hash__(self):
        return hash(self._as_tuple())

    def _collect_links(self, links: Iterable) -> Iterator[Hashable]:
        from tdm.datamodel.facts import MentionFact

        for m in links:
            if isinstance(m, MentionFact):
                yield m.mention

    def _collect_not_empty_links(self, id_: str, links: Iterable) -> Iterator[Hashable]:
        from tdm.abstract.datamodel.fact import AbstractLinkFact

        for p in links:
            if isinstance(p, AbstractLinkFact) and p.target.id == id_:
                yield p.str_type_id, p.source

    @staticmethod
    def empty_value_filter() -> Callable[['AtomValueFact'], bool]:
        """
        Create a filter function to filter `AtomValueFact` instances with empty values.

        :return: A filter function for `AtomValueFact` instances with empty values.
        """
        return lambda f: isinstance(f.value, tuple) and not f.value

    @staticmethod
    def tuple_value_filter() -> Callable[['AtomValueFact'], bool]:
        """
        Create a filter function to filter `AtomValueFact` instances with tuple values.

        :return: A filter function for `AtomValueFact` instances with tuple values.
        """
        return lambda f: isinstance(f.value, tuple)

    @staticmethod
    def single_value_filter() -> Callable[['AtomValueFact'], bool]:
        """
        Create a filter function to filter `AtomValueFact` instances with a single value.

        :return: A filter function for `AtomValueFact` instances with a single value.
        """
        return lambda f: isinstance(f.value, AbstractValue)

    def is_hanging(self, doc: ViewContainer) -> bool:
        from .mention import MentionFact
        return self.status is not FactStatus.APPROVED \
            and not self.value \
            and not tuple(doc.related_elements(AbstractFact, self, MentionFact, tuple()))

    def choose_one(
            self, other, related: Callable[[str], Iterable[str]], restore_element: Callable[[str], EnsureIdentifiable]
    ) -> Optional[Tuple[str, str]]:
        if not isinstance(other, type(self)) or self.str_type_id != other.str_type_id:
            return None
        if self.status is FactStatus.APPROVED and other.status is FactStatus.APPROVED:
            return None
        if self._tuple_value() != other._tuple_value():
            return None
        if not self.value:  # equal empty values => check links
            links = set(self._collect_links(map(restore_element, related(self.id))))
            other_links = set(self._collect_links(map(restore_element, related(other.id))))
            if not (links <= other_links or other_links <= links):
                return None
        else:
            links = set(self._collect_not_empty_links(self.id, map(restore_element, related(self.id))))
            other_links = set(self._collect_not_empty_links(other.id, map(restore_element, related(other.id))))
            if not (links <= other_links or other_links <= links):
                return None

        return (self.id, other.id) if self.status < other.status else (other.id, self.id)


@dataclass(frozen=True)
class _CompositeValueFact(AbstractFact, metaclass=ABCMeta):
    """
    Auxiliary class for `CompositeValueFact` to fix dataclass fields order.

    Attributes
    ----------
    type_id:
        The type identifier or domain composite value type of the composite value fact.
    """
    type_id: Union[str, CompositeValueType]

    @classmethod
    def constant_fields(cls) -> Set[str]:
        return {'type_id'}

    @property
    def str_type_id(self) -> str:
        return self.type_id if isinstance(self.type_id, str) else self.type_id.id


@generate_model(label='composite')
@dataclass(frozen=True)
class CompositeValueFact(Identifiable, _CompositeValueFact, PrunableMixin, Duplicatable):
    """
    Represents a fact that holds a composite value.

    The whole value is represented as `CompositeValueFact` with related `ComponentFact`s.
    """

    def replace_with_domain(self, domain: AbstractDomain) -> 'CompositeValueFact':
        if isinstance(self.type_id, str):
            domain_type = domain.get_type(self.type_id)
            if not isinstance(domain_type, CompositeValueType):
                raise ValueError
            return replace(self, type_id=domain_type)
        return self

    def _as_tuple(self) -> tuple:
        return self.id, self.str_type_id

    def __eq__(self, other):
        if not isinstance(other, CompositeValueFact):
            return NotImplemented
        return self._as_tuple() == other._as_tuple()

    def __hash__(self):
        return hash(self._as_tuple())

    def is_hanging(self, doc: ViewContainer) -> bool:
        return self.status is not FactStatus.APPROVED and \
            not [x.target for x in doc.related_elements(AbstractFact, self, ComponentFact, tuple())]

    def duplicate_hash(self) -> Hashable:
        return self.str_type_id

    @staticmethod
    def _collect_components(props) -> Iterator:
        for p in props:
            if isinstance(p, ComponentFact):
                yield p.str_type_id, p.target

    def choose_one(
            self, other, related: Callable[[str], Iterable[str]], restore_element: Callable[[str], EnsureIdentifiable]
    ) -> Optional[Tuple[str, str]]:
        if not isinstance(other, CompositeValueFact) or self.str_type_id != other.str_type_id:
            return None
        if self.status is FactStatus.APPROVED and other.status is FactStatus.APPROVED:
            return None
        props = set(self._collect_components(map(restore_element, related(self.id))))
        other_props = set(self._collect_components(map(restore_element, related(other.id))))
        if props <= other_props or other_props <= props:
            return (self.id, other.id) if self.status < other.status else (other.id, self.id)
        return None


ValueFact = Union[AtomValueFact, CompositeValueFact]


@generate_model(label='component')
@dataclass(frozen=True, eq=False)
class ComponentFact(Identifiable, AbstractLinkFact[CompositeValueFact, ValueFact, ComponentValueType]):
    """
    Represents a composite value component fact.
    It links composite value fact with another value fact (its component).
    """
    pass
