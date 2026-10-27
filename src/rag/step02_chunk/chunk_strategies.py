"""
Multiple chunking strategies for practice and comparison.

Each strategy returns the same TextChunk shape so the rest of the pipeline stays unchanged.
"""

from __future__ import annotations

import re
from enum import Enum
from typing import Protocol

import tiktoken

from src.core.config import get_settings
from src.domain.models import TextChunk
from src.rag.step02_chunk.chunker import TextChunker


class ChunkStrategy(str, Enum):
    """How we cut long text into smaller pieces."""

    TOKEN = "token"  # fixed token windows (default, matches TextChunker)
    SENTENCE = "sentence"  # split on sentence boundaries, then pack into token budget
    PARAGRAPH = "paragraph"  # one chunk per paragraph (blank-line separated)
    RECURSIVE = "recursive"  # try big separators first, then smaller ones


class ChunkerProtocol(Protocol):
    def chunk(self, text: str, metadata: dict | None = None) -> list[TextChunk]: ...


class SentenceChunker:
    """Pack sentences until each chunk is near chunk_size tokens."""

    def __init__(self) -> None:
        settings = get_settings()
        self.chunk_size = settings.chunk_size
        self.token_chunker = TextChunker()

    def chunk(self, text: str, metadata: dict | None = None) -> list[TextChunk]:
        metadata = metadata or {}
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return []

        packed: list[str] = []
        current: list[str] = []

        for sentence in sentences:
            candidate = " ".join(current + [sentence])
            if self.token_chunker.count_tokens(candidate) <= self.chunk_size:
                current.append(sentence)
            else:
                if current:
                    packed.append(" ".join(current))
                current = [sentence]
        if current:
            packed.append(" ".join(current))

        chunks: list[TextChunk] = []
        for index, piece in enumerate(packed):
            chunks.append(
                TextChunk(
                    content=piece,
                    chunk_index=index,
                    token_count=self.token_chunker.count_tokens(piece),
                    metadata={**metadata, "strategy": ChunkStrategy.SENTENCE.value},
                )
            )
        return chunks


class ParagraphChunker:
    """Split on blank lines; oversized paragraphs fall back to token chunking."""

    def __init__(self) -> None:
        self.token_chunker = TextChunker()
        settings = get_settings()
        self.chunk_size = settings.chunk_size

    def chunk(self, text: str, metadata: dict | None = None) -> list[TextChunk]:
        metadata = metadata or {}
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        if not paragraphs:
            return []

        chunks: list[TextChunk] = []
        index = 0
        for para in paragraphs:
            if self.token_chunker.count_tokens(para) > self.chunk_size:
                sub = self.token_chunker.chunk(
                    para, metadata={**metadata, "strategy": ChunkStrategy.PARAGRAPH.value}
                )
                for item in sub:
                    item.chunk_index = index
                    index += 1
                    chunks.append(item)
            else:
                chunks.append(
                    TextChunk(
                        content=para,
                        chunk_index=index,
                        token_count=self.token_chunker.count_tokens(para),
                        metadata={**metadata, "strategy": ChunkStrategy.PARAGRAPH.value},
                    )
                )
                index += 1
        return chunks


class RecursiveCharacterChunker:
    """
    LangChain-style recursive split: try \\n\\n, \\n, space, then characters.
    """

    def __init__(self) -> None:
        settings = get_settings()
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap
        self.encoding = tiktoken.get_encoding("cl100k_base")
        self.separators = ["\n\n", "\n", ". ", " ", ""]

    def _token_len(self, s: str) -> int:
        return len(self.encoding.encode(s))

    def _merge_splits(self, splits: list[str], metadata: dict) -> list[TextChunk]:
        chunks: list[TextChunk] = []
        current: list[str] = []
        current_len = 0
        index = 0

        def flush() -> None:
            nonlocal index, current, current_len
            if not current:
                return
            body = "".join(current).strip()
            if body:
                chunks.append(
                    TextChunk(
                        content=body,
                        chunk_index=index,
                        token_count=self._token_len(body),
                        metadata={**metadata, "strategy": ChunkStrategy.RECURSIVE.value},
                    )
                )
                index += 1
            current = []
            current_len = 0

        for piece in splits:
            piece_len = self._token_len(piece)
            if piece_len > self.chunk_size:
                flush()
                token_chunker = TextChunker()
                for sub in token_chunker.chunk(piece, metadata=metadata):
                    sub.chunk_index = index
                    sub.metadata["strategy"] = ChunkStrategy.RECURSIVE.value
                    chunks.append(sub)
                    index += 1
                continue
            if current_len + piece_len > self.chunk_size:
                flush()
            current.append(piece)
            current_len += piece_len
        flush()
        return chunks

    def _split_text(self, text: str, separators: list[str]) -> list[str]:
        if not separators:
            return list(text)
        sep = separators[0]
        rest = separators[1:]
        if sep == "":
            return list(text)
        parts = text.split(sep)
        out: list[str] = []
        for i, part in enumerate(parts):
            suffix = sep if i < len(parts) - 1 else ""
            merged = part + suffix
            if self._token_len(merged) > self.chunk_size and rest:
                out.extend(self._split_text(merged, rest))
            else:
                out.append(merged)
        return out

    def chunk(self, text: str, metadata: dict | None = None) -> list[TextChunk]:
        metadata = metadata or {}
        splits = self._split_text(text, self.separators)
        return self._merge_splits(splits, metadata)


def get_chunker(strategy: ChunkStrategy | str = ChunkStrategy.TOKEN) -> ChunkerProtocol:
    """Factory used by validation scripts and experiments."""
    if isinstance(strategy, str):
        strategy = ChunkStrategy(strategy)
    if strategy == ChunkStrategy.TOKEN:
        return TextChunker()
    if strategy == ChunkStrategy.SENTENCE:
        return SentenceChunker()
    if strategy == ChunkStrategy.PARAGRAPH:
        return ParagraphChunker()
    if strategy == ChunkStrategy.RECURSIVE:
        return RecursiveCharacterChunker()
    raise ValueError(f"Unknown chunk strategy: {strategy}")
