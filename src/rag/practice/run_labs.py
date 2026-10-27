"""
Hands-on RAG labs (offline-friendly).

    python -m src.rag.practice.run_labs
    python -m src.rag.practice.run_labs --lab 3
"""

from __future__ import annotations

import argparse
import json

from src.rag.step02_chunk.offline_chunks import split_markdown_sections
from src.rag.step02_chunk.parent_child import ParentChildChunker
from src.rag.step05_retrieve.bm25_index import Bm25Index, reciprocal_rank_fusion
from src.rag.step05_retrieve.query_transform import transform_query
from src.rag.step08_evaluate.run_practice_eval import run_offline


def lab_1_chunking(corpus: str) -> None:
    print("=== Lab 1: Section chunking (offline) ===")
    sections = split_markdown_sections(corpus)
    print(f"  markdown sections: {len(sections)}")
    print("  (With network/API: compare token/sentence/recursive via validate_chunking)")


def lab_2_parent_child(corpus: str) -> None:
    print("=== Lab 2: Parent–child chunking ===")
    try:
        bundle = ParentChildChunker().chunk(corpus)
    except Exception as exc:
        print(f"  skipped (needs tiktoken/OpenAI encoding cache): {exc}")
        return
    print(f"  parents: {len(bundle.parents)}, children: {len(bundle.children)}")
    print(f"  sample child metadata: {bundle.children[0].metadata}")


def lab_3_hybrid(corpus: str) -> None:
    print("=== Lab 3: BM25 + RRF fusion ===")
    section_texts = split_markdown_sections(corpus)
    index = Bm25Index()
    ids = [f"c{i}" for i in range(len(section_texts))]
    index.add_many(ids, section_texts)
    query = "VPN access for remote employees"
    bm25_hits = index.search(query, top_k=3)
    vector_guess = [ids[0], ids[2], ids[5]] if len(ids) > 5 else ids[:3]
    fused = reciprocal_rank_fusion([vector_guess, [h.doc_id for h in bm25_hits]])
    print(f"  query: {query}")
    print(f"  BM25 top: {[h.doc_id for h in bm25_hits]}")
    print(f"  RRF fused order: {[x[0] for x in fused[:5]]}")


def lab_4_query_transform() -> None:
    print("=== Lab 4: Query transform (acronyms) ===")
    q = "What is our SLA for VPN incidents?"
    t = transform_query(q)
    print(f"  original:  {t.original}")
    print(f"  rewritten: {t.rewritten}")
    print(f"  notes: {t.notes}")


def lab_5_eval() -> None:
    print("=== Lab 5: Offline evaluation report ===")
    report = run_offline(mock_retrieval=True)
    print(json.dumps(report, indent=2))


def main() -> None:
    from src.core.config import get_settings

    corpus_path = (
        get_settings().base_dir / "data" / "examples" / "corpus" / "enterprise_it_runbook.md"
    )
    corpus = corpus_path.read_text(encoding="utf-8")

    parser = argparse.ArgumentParser()
    parser.add_argument("--lab", type=int, choices=[1, 2, 3, 4, 5])
    args = parser.parse_args()

    labs = {
        1: lambda: lab_1_chunking(corpus),
        2: lambda: lab_2_parent_child(corpus),
        3: lambda: lab_3_hybrid(corpus),
        4: lab_4_query_transform,
        5: lab_5_eval,
    }

    if args.lab:
        labs[args.lab]()
        return

    for fn in labs.values():
        fn()
        print()


if __name__ == "__main__":
    main()
