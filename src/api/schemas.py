from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.core.enums import SourceType


class IngestRequest(BaseModel):
    source_type: SourceType
    source_uri: str = Field(..., description="Local file path or URL")


class IngestResponse(BaseModel):
    job_id: UUID
    document_id: UUID | None = None
    status: str
    message: str


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=2000)


class SourceChunk(BaseModel):
    chunk_id: UUID
    content: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    latency_ms: float


class DocumentResponse(BaseModel):
    id: UUID
    title: str
    source_type: str
    source_uri: str
    status: str
    created_at: datetime