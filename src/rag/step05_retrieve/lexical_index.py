"""Shared BM25 index updated when documents are indexed."""

from __future__ import annotations

from src.rag.step05_retrieve.bm25_index import Bm25Index

_index: Bm25Index | None = None


def get_lexical_index() -> Bm25Index:
    global _index
    if _index is None:
        _index = Bm25Index()
        _index.load()
    return _index
