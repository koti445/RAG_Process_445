from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

@dataclass
class LoadedDocument:
    content: str
    source_type: str
    source_uri: str
    metadata: dict[str, Any] = field(default_factory=dict)
    
@dataclass
class TextChunk:
    content: str
    chunk_index: int
    token_count: int
    metadata: dict[str, Any] = field(default_factory=dict)
    
    
@dataclass
class RetrievalResult:
    chunk_id: UUID
    content: str
    score: float
    metadata: dict[str, Any]
    

@dataclass
class RAGResponse:
    answer: str
    sources: list[RetrievalResult]