import pytest

from src.rag.step06_generate.generator import Generator


def test_generator_without_context():
    generator = Generator()
    answer = generator.generate("What is RAG?", [])
    assert "don't have enough information" in answer.lower()


@pytest.mark.skip(reason="Requires valid OPENAI_API_KEY")
def test_generator_with_context():
    generator = Generator()
    answer = generator.generate(
        "What is RAG?",
        ["RAG stands for Retrieval-Augmented Generation."],
    )
    assert "retrieval" in answer.lower()