import math

import pytest

from src.rag.step03_embed.embedder import Embedder
from src.rag.step03_embed.embedding_utils import (
    cosine_similarity,
    validate_vector_structure,
)


def test_embed_texts_empty_returns_empty():
    embedder = Embedder()
    assert embedder.embed_texts([]) == []


def test_cosine_similarity_identical_vectors():
    v = [1.0, 0.0, 0.0]
    assert math.isclose(cosine_similarity(v, v), 1.0)


def test_cosine_similarity_orthogonal():
    a = [1.0, 0.0]
    b = [0.0, 1.0]
    assert math.isclose(cosine_similarity(a, b), 0.0)


def test_validate_vector_structure_ok():
    vec = [0.1, 0.2, 0.3]
    result = validate_vector_structure(vec, expected_dim=3)
    assert result["ok"] is True
    assert result["dim"] == 3


def test_validate_vector_structure_wrong_dim():
    result = validate_vector_structure([0.1, 0.2], expected_dim=3)
    assert result["ok"] is False
    assert "expected 3" in result["issues"][0]


@pytest.mark.skip(reason="Requires valid OPENAI_API_KEY")
def test_embed_query_openai_integration():
    embedder = Embedder()
    vector = embedder.embed_query("hello world")

    assert isinstance(vector, list)
    assert len(vector) == 1536  # text-embedding-3-small default
    assert validate_vector_structure(vector, expected_dim=1536)["ok"]
