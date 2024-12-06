from enum import Enum
from typing import Dict, Optional, Tuple

from pydantic import BaseModel


class NodeType(Enum):
    HEADER = "header"
    TEXT = "text"
    LIST = "list"
    JSON = "json"
    KEY = "key"
    TABLE = "table"
    TABLE_ROW = "row"
    IMAGE = "image"


class NodeMetadata(BaseModel):
    node_type: NodeType
    original_text: Optional[str]
    text_translations: Dict[str, str] = {}
    language: Optional[str] = None
    hidden: bool = False

    class Config:
        extra = 'allow'  # any other extra fields will be kept


class NodeMarkup(BaseModel):
    class Config:
        extra = 'allow'  # any other extra fields will be kept


class TreeDocumentContentModel(BaseModel):
    id: str
    metadata: NodeMetadata
    text: str
    nodes: Optional[Tuple['TreeDocumentContentModel', ...]]
    markup: NodeMarkup = NodeMarkup()


TreeDocumentContentModel.update_forward_refs()
