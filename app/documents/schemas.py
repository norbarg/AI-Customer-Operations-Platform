from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class DocumentSource(StrEnum):
    manual = "manual"
    upload = "upload"


class DocumentStatus(StrEnum):
    pending = "pending"
    processing = "processing"
    chunked = "chunked"
    ready = "ready"
    failed = "failed"


class DocumentCreate(BaseModel):
    title: str
    source: DocumentSource = DocumentSource.manual
    file_name: str | None = None
    mime_type: str | None = None
    content: str | None = None


class DocumentUpdate(BaseModel):
    title: str | None = None
    source: DocumentSource | None = None
    file_name: str | None = None
    mime_type: str | None = None
    content: str | None = None
    status: DocumentStatus | None = None


class DocumentResponse(BaseModel):
    id: int
    title: str
    source: DocumentSource
    file_name: str | None
    mime_type: str | None
    content: str | None
    status: DocumentStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentChunkResponse(BaseModel):
    id: int
    document_id: int
    chunk_index: int
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
