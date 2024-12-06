from typing import Any, Dict, Optional, Tuple, Union

from pydantic import BaseModel


class MetadataModel(BaseModel):
    def to_metadata(self) -> Dict[str, Any]:
        return self.dict(exclude_none=True)


class FactMetadataModel(MetadataModel):
    created_time: Optional[int]
    modified_time: Optional[int]
    fact_confidence: Optional[Tuple[float]]
    value_confidence: Union[float, Tuple[float, ...], None]  # same as Optional[float, Tuple[float, ...]] (pydantic bug workaround)

    class Config:
        extra = 'allow'  # any other extra fields will be kept


class DocumentMetadataModel(MetadataModel):
    title: Optional[str]
    file_name: Optional[str]
    file_type: Optional[str]
    size: Optional[int]
    created_time: Optional[int]
    access_time: Optional[int]
    modified_time: Optional[int]
    publication_date: Optional[int]
    publication_author: Optional[str]
    description: Optional[str]
    language: Optional[str]
    parent_uuid: Optional[str]
    url: Optional[str]
    platform: Optional[str]
    account: Optional[Tuple[str, ...]]
    access_level: Optional[str]
    user: Optional[str]
    path: Optional[str]
    trust_level: Optional[float]
    markers: Optional[Tuple[str, ...]]
    related_concept_id: Optional[str]
    preview_text: Optional[str]
    story: Optional[str]

    class Config:
        extra = 'allow'  # any other extra fields will be kept
