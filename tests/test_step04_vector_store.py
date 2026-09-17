from src.rag.step04_store.vector_store import VectorStore


def test_vector_store_add_and_search(tmp_path, monkeypatch):
    monkeypatch.setenv("CHROMA_PERSIST_DIR", str(tmp_path / "chroma"))

    from src.core.config import get_settings

    get_settings.cache_clear()

    store = VectorStore(collection_name="test_collection")
    store.add(
        ids=["1"],
        embeddings=[[1.0, 0.0, 0.0]],
        documents=["hello world"],
        metadatas=[{"source": "test"}],
    )

    result = store.search([1.0, 0.0, 0.0], top_k=1)
    assert result["ids"][0][0] == "1"