from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal
from enum import Enum


class DocumentType(str, Enum):
    TXT = "txt"
    IMG = "img"
    PDF = "pdf"


class DocumentCreate(BaseModel):
    filename: str
    file_type: DocumentType
    file_size: int
    content: Optional[str] = None  # For text files and extracted PDF text


class DocumentInDB(BaseModel):
    id: str
    filename: str
    file_type: DocumentType
    file_path: str
    file_size: int
    upload_date: datetime
    content: Optional[str] = None
    metadata: Optional[dict] = None


class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_type: DocumentType
    file_size: int
    upload_date: datetime
    metadata: Optional[dict] = None


class DocumentPreview(BaseModel):
    id: str
    filename: str
    file_type: DocumentType
    content: Optional[str] = None
    file_url: Optional[str] = None  # For images