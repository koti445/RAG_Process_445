"""Demo BM25 + RRF on enterprise practice corpus (no OpenAI)."""

from __future__ import annotations

from src.core.config import get_settings
from src.rag.step02_chunk.offline_chunks import split_markdown_sections
from src.rag.step05_retrieve.bm25_index import Bm25Index, reciprocal_rank_fusion


def main() -> None:
    path = get_settings().base_dir / "data" / "examples" / "corpus" / "enterprise_hr_policy.md"
    text = path.read_text(encoding="utf-8")
    section_texts = split_markdown_sections(text)
    index = Bm25Index()
    ids = [f"hr_{i}" for i in range(len(section_texts))]
    index.add_many(ids, section_texts)

    queries = [
        "How many days of annual leave?",
        "PII data handling",
        "performance review cycle",
    ]
    print(f"Indexed {len(section_texts)} sections from {path.name}\n")
    for query in queries:
        hits = index.search(query, top_k=3)
        print(f"Q: {query}")
        for h in hits:
            snippet = section_texts[int(h.doc_id.split("_")[1])][:80].replace("\n", " ")
            print(f"   {h.doc_id} score={h.score:.3f} | {snippet}...")
        fake_vector = [hits[0].doc_id] if hits else []
        rrf = reciprocal_rank_fusion([fake_vector, [h.doc_id for h in hits]])
        print(f"   RRF top: {rrf[0][0] if rrf else 'n/a'}\n")


if __name__ == "__main__":
    main()
