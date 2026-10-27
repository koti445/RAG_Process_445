"""
Reranking: reorder retrieved chunks so the best ones appear first.

Practice order:
1. PassthroughReranker — no change (baseline)
2. LexicalReranker — boost chunks that share words with the question (no extra models)
3. Optional cross-encoder — install sentence-transformers and set RERANK_CROSS_ENCODER model name
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from src.domain.models import RetrievalResult


def _tokenize(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if len(t) > 2}


@dataclass
class RerankConfig:
    lexical_weight: float = 0.35
    vector_weight: float = 0.65


class PassthroughReranker:
    def rerank(self, question: str, results: list[RetrievalResult]) -> list[RetrievalResult]:
        return results


class LexicalReranker:
    """Combine vector score with simple keyword overlap (good for learning retrieval quality)."""

    def __init__(self, config: RerankConfig | None = None) -> None:
        self.config = config or RerankConfig()

    def rerank(self, question: str, results: list[RetrievalResult]) -> list[RetrievalResult]:
        if not results:
            return results
        q_tokens = _tokenize(question)
        if not q_tokens:
            return results

        scored: list[tuple[float, RetrievalResult]] = []
        for item in results:
            doc_tokens = _tokenize(item.content)
            overlap = len(q_tokens & doc_tokens) / max(len(q_tokens), 1)
            combined = self.config.vector_weight * item.score + self.config.lexical_weight * overlap
            scored.append((combined, item))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        out: list[RetrievalResult] = []
        for combined, item in scored:
            out.append(
                RetrievalResult(
                    chunk_id=item.chunk_id,
                    content=item.content,
                    score=combined,
                    metadata={**item.metadata, "rerank": "lexical"},
                )
            )
        return out


class CrossEncoderReranker:
    """
    Uses sentence-transformers CrossEncoder when installed.
    Model example: cross-encoder/ms-marco-MiniLM-L-6-v2
    """

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._model = None

    def _load(self) -> None:
        if self._model is not None:
            return
        try:
            from sentence_transformers import CrossEncoder
        except ImportError as exc:
            raise ImportError(
                "Install optional rerank deps: pip install sentence-transformers"
            ) from exc
        self._model = CrossEncoder(self.model_name)

    def rerank(self, question: str, results: list[RetrievalResult]) -> list[RetrievalResult]:
        if not results:
            return results
        self._load()
        pairs = [[question, r.content] for r in results]
        scores = self._model.predict(pairs)
        ranked = sorted(zip(scores, results), key=lambda x: float(x[0]), reverse=True)
        out: list[RetrievalResult] = []
        for score, item in ranked:
            out.append(
                RetrievalResult(
                    chunk_id=item.chunk_id,
                    content=item.content,
                    score=float(score),
                    metadata={**item.metadata, "rerank": "cross_encoder"},
                )
            )
        return out


def get_reranker(mode: str, cross_encoder_model: str = "") -> PassthroughReranker | LexicalReranker | CrossEncoderReranker:
    mode = (mode or "none").lower()
    if mode in {"none", "off", "passthrough"}:
        return PassthroughReranker()
    if mode in {"lexical", "keyword"}:
        return LexicalReranker()
    if mode in {"cross_encoder", "cross-encoder"}:
        if not cross_encoder_model:
            cross_encoder_model = "cross-encoder/ms-marco-MiniLM-L-6-v2"
        return CrossEncoderReranker(cross_encoder_model)
    raise ValueError(f"Unknown rerank mode: {mode}")
