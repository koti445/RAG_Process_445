import uuid

from src.domain.models import RetrievalResult
from src.rag.step05_retrieve.reranker import LexicalReranker


def test_lexical_reranker_promotes_matching_chunk():
    question = "laptop warranty duration"
    results = [
        RetrievalResult(
            chunk_id=uuid.uuid4(),
            content="Shipping takes five to seven days.",
            score=0.9,
            metadata={},
        ),
        RetrievalResult(
            chunk_id=uuid.uuid4(),
            content="Laptop warranty is twenty four months.",
            score=0.7,
            metadata={},
        ),
    ]
    reranked = LexicalReranker().rerank(question, results)
    assert "warranty" in reranked[0].content.lower()
