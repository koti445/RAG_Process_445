"""Offline retrieval metrics — no API keys required."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class RetrievalMetrics:
    precision_at_k: float
    recall_at_k: float
    mrr: float
    ndcg_at_k: float
    hit_at_k: bool


def precision_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float:
    top_k = retrieved_ids[:k]
    if not top_k:
        return 0.0
    hits = sum(1 for item_id in top_k if item_id in relevant_ids)
    return hits / len(top_k)


def recall_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float:
    if not relevant_ids:
        return 0.0
    top_k = retrieved_ids[:k]
    hits = sum(1 for item_id in top_k if item_id in relevant_ids)
    return hits / len(relevant_ids)


def reciprocal_rank(retrieved_ids: list[str], relevant_ids: set[str]) -> float:
    for rank, item_id in enumerate(retrieved_ids, start=1):
        if item_id in relevant_ids:
            return 1.0 / rank
    return 0.0


def dcg_at_k(relevances: list[int], k: int) -> float:
    score = 0.0
    for i, rel in enumerate(relevances[:k], start=1):
        score += (2**rel - 1) / math.log2(i + 1)
    return score


def ndcg_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float:
    relevances = [1 if item_id in relevant_ids else 0 for item_id in retrieved_ids]
    ideal = sorted(relevances, reverse=True)
    ideal_dcg = dcg_at_k(ideal, k)
    if ideal_dcg == 0:
        return 0.0
    return dcg_at_k(relevances, k) / ideal_dcg


def compute_retrieval_metrics(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> RetrievalMetrics:
    return RetrievalMetrics(
        precision_at_k=precision_at_k(retrieved_ids, relevant_ids, k),
        recall_at_k=recall_at_k(retrieved_ids, relevant_ids, k),
        mrr=reciprocal_rank(retrieved_ids, relevant_ids),
        ndcg_at_k=ndcg_at_k(retrieved_ids, relevant_ids, k),
        hit_at_k=any(item_id in relevant_ids for item_id in retrieved_ids[:k]),
    )
