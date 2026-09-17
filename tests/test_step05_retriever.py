import pytest

from src.rag.step05_retrieve.retriever import Retriever


@pytest.mark.skip(reason="Requires indexed vectors and OPENAI_API_KEY")
def test_retriever():
    retriever = Retriever()
    results = retriever.retrieve("test question")
    assert isinstance(results, list)