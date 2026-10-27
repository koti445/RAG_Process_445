from src.rag.step02_chunk.chunk_strategies import ChunkStrategy, get_chunker


def test_all_strategies_produce_chunks():
    text = "First sentence. Second sentence.\n\nSecond paragraph with more words.\n" * 50
    for strategy in ChunkStrategy:
        chunks = get_chunker(strategy).chunk(text)
        assert len(chunks) >= 1
        assert chunks[0].token_count > 0


def test_paragraph_strategy_keeps_sections():
    text = "Part A.\n\nPart B is separate."
    chunks = get_chunker(ChunkStrategy.PARAGRAPH).chunk(text)
    assert len(chunks) == 2
