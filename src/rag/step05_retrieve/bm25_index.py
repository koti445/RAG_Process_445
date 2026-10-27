"""
Okapi BM25 lexical search for learning hybrid RAG (no extra dependencies).

Enterprise teams often combine BM25 (exact keyword match) with vectors (semantic match).
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from pathlib import Path

from src.core.config import get_settings

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


@dataclass
class Bm25Hit:
    doc_id: str
    score: float


class Bm25Index:
    """In-memory BM25 over chunk ids; persisted as JSON for practice restarts."""

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self._docs: dict[str, list[str]] = {}
        self._avg_dl = 0.0
        self._df: dict[str, int] = {}
        self._N = 0

    @property
    def persist_path(self) -> Path:
        return get_settings().data_processed_dir / "bm25_index.json"

    def add(self, doc_id: str, text: str) -> None:
        tokens = _tokenize(text)
        self._docs[doc_id] = tokens
        self._rebuild_stats()

    def add_many(self, doc_ids: list[str], texts: list[str]) -> None:
        for doc_id, text in zip(doc_ids, texts):
            self._docs[doc_id] = _tokenize(text)
        self._rebuild_stats()

    def _rebuild_stats(self) -> None:
        self._N = len(self._docs)
        if self._N == 0:
            self._avg_dl = 0.0
            self._df = {}
            return
        lengths = [len(t) for t in self._docs.values()]
        self._avg_dl = sum(lengths) / len(lengths)
        df: dict[str, int] = {}
        for tokens in self._docs.values():
            for term in set(tokens):
                df[term] = df.get(term, 0) + 1
        self._df = df

    def search(self, query: str, top_k: int = 5) -> list[Bm25Hit]:
        if not self._docs:
            return []
        q_terms = _tokenize(query)
        if not q_terms:
            return []

        scores: list[Bm25Hit] = []
        for doc_id, tokens in self._docs.items():
            dl = len(tokens)
            tf_map: dict[str, int] = {}
            for t in tokens:
                tf_map[t] = tf_map.get(t, 0) + 1
            score = 0.0
            for term in q_terms:
                if term not in tf_map:
                    continue
                df = self._df.get(term, 0)
                idf = math.log(1 + (self._N - df + 0.5) / (df + 0.5))
                tf = tf_map[term]
                denom = tf + self.k1 * (1 - self.b + self.b * dl / max(self._avg_dl, 1))
                score += idf * (tf * (self.k1 + 1)) / denom
            if score > 0:
                scores.append(Bm25Hit(doc_id=doc_id, score=score))
        scores.sort(key=lambda h: h.score, reverse=True)
        return scores[:top_k]

    def save(self) -> None:
        path = self.persist_path
        payload = {"docs": {k: " ".join(v) for k, v in self._docs.items()}}
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load(self) -> bool:
        path = self.persist_path
        if not path.exists():
            return False
        raw = json.loads(path.read_text(encoding="utf-8"))
        docs = raw.get("docs", {})
        self._docs = {k: _tokenize(v) for k, v in docs.items()}
        self._rebuild_stats()
        return True


def reciprocal_rank_fusion(
    ranked_lists: list[list[str]],
    k: int = 60,
) -> list[tuple[str, float]]:
    """
    RRF score = sum(1 / (k + rank)) across lists.
    Standard enterprise fusion when vector and BM25 scales differ.
    """
    scores: dict[str, float] = {}
    for ranked in ranked_lists:
        for rank, doc_id in enumerate(ranked, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
