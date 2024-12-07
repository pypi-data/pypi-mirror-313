from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class TextractBlockType(str, Enum):
    KEY_VALUE_SET = 'KEY_VALUE_SET'
    PAGE = 'PAGE'
    LINE = 'LINE'
    WORD = 'WORD'
    TABLE = 'TABLE'
    CELL = 'CELL'
    SELECTION_ELEMENT = 'SELECTION_ELEMENT'
    MERGED_CELL = 'MERGED_CELL'
    TITLE = 'TITLE'
    QUERY = 'QUERY'
    QUERY_RESULT = 'QUERY_RESULT'
    SIGNATURE = 'SIGNATURE'
    TABLE_TITLE = 'TABLE_TITLE'
    TABLE_FOOTER = 'TABLE_FOOTER'
    LAYOUT_TEXT = 'LAYOUT_TEXT'
    LAYOUT_TITLE = 'LAYOUT_TITLE'
    LAYOUT_HEADER = 'LAYOUT_HEADER'
    LAYOUT_FOOTER = 'LAYOUT_FOOTER'
    LAYOUT_SECTION_HEADER = 'LAYOUT_SECTION_HEADER'
    LAYOUT_PAGE_NUMBER = 'LAYOUT_PAGE_NUMBER'
    LAYOUT_LIST = 'LAYOUT_LIST'
    LAYOUT_FIGURE = 'LAYOUT_FIGURE'
    LAYOUT_TABLE = 'LAYOUT_TABLE'
    LAYOUT_KEY_VALUE = 'LAYOUT_KEY_VALUE'


class TextractTextTypeEnum(str, Enum):
    HANDWRITING = 'HANDWRITING'
    PRINTED = 'PRINTED'


class TextractRelationshipType(str, Enum):
    VALUE = 'VALUE'
    CHILD = 'CHILD'
    COMPLEX_FEATURES = 'COMPLEX_FEATURES'
    MERGED_CELL = 'MERGED_CELL'
    TITLE = 'TITLE'
    ANSWER = 'ANSWER'
    TABLE = 'TABLE'
    TABLE_TITLE = 'TABLE_TITLE'
    TABLE_FOOTER = 'TABLE_FOOTER'


class TextractEntityTypes(str, Enum):
    KEY = 'KEY'
    VALUE = 'VALUE'
    COLUMN_HEADER = 'COLUMN_HEADER'
    TABLE_TITLE = 'TABLE_TITLE'
    TABLE_FOOTER = 'TABLE_FOOTER'
    TABLE_SECTION_TITLE = 'TABLE_SECTION_TITLE'
    TABLE_SUMMARY = 'TABLE_SUMMARY'
    STRUCTURED_TABLE = 'STRUCTURED_TABLE'
    SEMI_STRUCTURED_TABLE = 'SEMI_STRUCTURED_TABLE'


class TextractSelectionStatus(str, Enum):
    SELECTED = 'SELECTED'
    NOT_SELECTED = 'NOT_SELECTED'


class TextractBoundingBox(BaseModel):
    Width: Optional[float] = None
    Height: Optional[float] = None
    Left: Optional[float] = None
    Top: Optional[float] = None


class TextractPolygon(BaseModel):
    X: Optional[float] = None
    Y: Optional[float] = None


class TextractGeometry(BaseModel):
    BoundingBox: Optional[TextractBoundingBox] = None
    Polygon: Optional[List[TextractPolygon]] = None


class TextractRelationship(BaseModel):
    Type: Optional[TextractRelationshipType] = None
    Ids: Optional[List[str]] = None


class TextractQuery(BaseModel):
    Text: Optional[str] = None
    Alias: Optional[str] = None
    Pages: Optional[List[str]] = None


class TextractBlock(BaseModel):
    BlockType: Optional[TextractBlockType] = None
    Confidence: Optional[float] = None
    Text: Optional[str] = None
    TextType: Optional[TextractTextTypeEnum] = None
    RowIndex: Optional[int] = None
    ColumnIndex: Optional[int] = None
    RowSpan: Optional[int] = None
    ColumnSpan: Optional[int] = None
    Geometry: Optional[TextractGeometry] = None
    Id: Optional[str] = None
    Relationships: Optional[List[TextractRelationship]] = None
    EntityTypes: Optional[List[TextractEntityTypes]] = None
    SelectionStatus: Optional[TextractSelectionStatus] = None
    Page: Optional[int] = None
    Query: Optional[TextractQuery] = None


class TextractDocumentMetadata(BaseModel):
    Pages: Optional[int] = None


class TextractResponse(BaseModel):
    DocumentMetadata: Optional[TextractDocumentMetadata] = None
    Blocks: Optional[List[TextractBlock]] = None
    DetectDocumentTextModelVersion: Optional[str] = None
