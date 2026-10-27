"""
Compare chunking strategies on the practice corpus.

    python -m src.rag.step02_chunk.validate_chunking
"""

from __future__ import annotations

from src.core.config import get_settings
from src.rag.step02_chunk.chunk_strategies import ChunkStrategy, get_chunker


def main() -> None:
    path = get_settings().base_dir / "data" / "examples" / "corpus" / "acme_support_faq.md"
    text = path.read_text(encoding="utf-8")

    print(f"Corpus: {path.name} ({len(text)} chars)\n")
    for strategy in ChunkStrategy:
        chunker = get_chunker(strategy)
        chunks = chunker.chunk(text, metadata={"source": path.name})
        sizes = [c.token_count for c in chunks]
        print(f"{strategy.value:12} -> {len(chunks)} chunks, tokens min/avg/max: "
              f"{min(sizes) if sizes else 0}/"
              f"{(sum(sizes) / len(sizes)) if sizes else 0:.0f}/"
              f"{max(sizes) if sizes else 0}")


if __name__ == "__main__":
    main()
