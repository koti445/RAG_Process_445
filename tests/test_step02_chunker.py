from src.rag.step02_chunk.chunker import TextChunker


def test_chunker_creates_multiple_chunks():
    chunker = TextChunker()
    text = "word " * 2000
    chunks = chunker.chunk(text)

    assert len(chunks) > 1
    assert chunks[0].chunk_index == 0
    assert chunks[0].token_count > 0