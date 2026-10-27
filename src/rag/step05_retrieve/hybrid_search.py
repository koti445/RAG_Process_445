"""Combine vector retrieval with BM25 using reciprocal rank fusion (RRF)."""

from __future__ import annotations

import uuid

from src.domain.models import RetrievalResult
from src.rag.step05_retrieve.bm25_index import Bm25Index, reciprocal_rank_fusion


def fuse_vector_and_lexical(
    question: str,
    vector_results: list[RetrievalResult],
    lexical_index: Bm25Index,
    top_k: int,
    fetch_k: int | None = None,
) -> list[RetrievalResult]:
    """
    Re-rank vector hits with BM25 RRF. Chunk ids must match between stores.
    """
    if not vector_results and not lexical_index._docs:
        return []

    fetch_k = fetch_k or max(top_k * 2, 10)
    vector_ranked = [str(r.chunk_id) for r in vector_results[:fetch_k]]
    lexical_hits = lexical_index.search(question, top_k=fetch_k)
    lexical_ranked = [h.doc_id for h in lexical_hits]

    fused = reciprocal_rank_fusion([vector_ranked, lexical_ranked])[:top_k]
    by_id = {str(r.chunk_id): r for r in vector_results}

    # Lexical-only hits: build minimal RetrievalResult if we have text in index only
    out: list[RetrievalResult] = []
    for doc_id, rrf_score in fused:
        if doc_id in by_id:
            base = by_id[doc_id]
            out.append(
                RetrievalResult(
                    chunk_id=base.chunk_id,
                    content=base.content,
                    score=rrf_score,
                    metadata={**base.metadata, "fusion": "rrf"},
                )
            )
        else:
            try:
                cid = uuid.UUID(doc_id)
            except ValueError:
                continue
            out.append(
                RetrievalResult(
                    chunk_id=cid,
                    content="",
                    score=rrf_score,
                    metadata={"fusion": "rrf", "lexical_only": True},
                )
            )
    return out
