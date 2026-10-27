"""
Parent–child chunking (enterprise pattern).

- **Child** chunks: small pieces → better embedding precision.
- **Parent** chunks: larger sections → shown to the LLM for context.

Children store parent_id in metadata; at query time you retrieve children then expand to parents.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from src.domain.models import TextChunk
from src.rag.step02_chunk.chunker import TextChunker


@dataclass
class ParentChildBundle:
    parents: list[TextChunk]
    children: list[TextChunk]


class ParentChildChunker:
    def __init__(self, parent_chunk_size: int = 800, child_chunk_size: int = 250) -> None:
        self.parent_chunker = TextChunker()
        self.parent_chunker.chunk_size = parent_chunk_size
        self.child_chunker = TextChunker()
        self.child_chunker.chunk_size = child_chunk_size

    def chunk(self, text: str, metadata: dict | None = None) -> ParentChildBundle:
        metadata = metadata or {}
        parents = self.parent_chunker.chunk(text, metadata={**metadata, "chunk_role": "parent"})
        children: list[TextChunk] = []

        for parent in parents:
            parent_id = str(uuid.uuid4())
            parent.metadata = {**parent.metadata, "parent_id": parent_id}
            sub_chunks = self.child_chunker.chunk(
                parent.content,
                metadata={
                    **metadata,
                    "chunk_role": "child",
                    "parent_id": parent_id,
                    "parent_index": parent.chunk_index,
                },
            )
            for child in sub_chunks:
                children.append(child)
        return ParentChildBundle(parents=parents, children=children)
