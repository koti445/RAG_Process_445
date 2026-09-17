import pytest

from src.rag.step03_embed.embedder import Embedder


@pytest.mark.skip(reason="Requires valid OPENAI_API_KEY")
def test_embed_query():
    embedder = Embedder()
    vector = embedder.embed_query("hello world")

    assert isinstance(vector, list)
    assert len(vector) > 0