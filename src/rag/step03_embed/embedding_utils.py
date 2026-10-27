"""Helpers for validating OpenAI embedding vectors (no Hugging Face dependency)."""

from __future__ import annotations

import math
from typing import Any

# Known output sizes for OpenAI embedding models
OPENAI_EMBEDDING_DIMS: dict[str, int] = {
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
    "text-embedding-ada-002": 1536,
}


def expected_dim_for_model(model_name: str) -> int | None:
    return OPENAI_EMBEDDING_DIMS.get(model_name)


def l2_norm(vector: list[float]) -> float:
    return math.sqrt(sum(x * x for x in vector))


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = l2_norm(a)
    norm_b = l2_norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def validate_vector_structure(
    vector: list[float],
    expected_dim: int | None = None,
) -> dict[str, Any]:
    issues: list[str] = []
    if not vector:
        issues.append("vector is empty")
    if any(not isinstance(x, (int, float)) for x in vector):
        issues.append("vector contains non-numeric values")
    if expected_dim is not None and len(vector) != expected_dim:
        issues.append(f"length {len(vector)} != expected {expected_dim}")
    norm = l2_norm(vector) if vector else 0.0
    if vector and norm == 0:
        issues.append("zero vector (all zeros)")
    return {
        "ok": len(issues) == 0,
        "dim": len(vector),
        "l2_norm": norm,
        "issues": issues,
    }
