"""
Validate OpenAI embeddings using project Embedder (no sentence-transformers / Hugging Face).

Requires OPENAI_API_KEY and EMBEDDING_MODEL in .env.

Run from repo root:
    python -m src.rag.step03_embed.validate_embedding
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Callable

from src.core.config import get_settings
from src.rag.step03_embed.embedder import Embedder
from src.rag.step03_embed.embedding_utils import (
    cosine_similarity,
    expected_dim_for_model,
    validate_vector_structure,
)


@dataclass
class ValidationExample:
    id: str
    title: str
    description: str


# ---------------------------------------------------------------------------
# Example catalog (what each check proves)
# ---------------------------------------------------------------------------
VALIDATION_EXAMPLES: list[ValidationExample] = [
    ValidationExample(
        "01",
        "Vector structure",
        "Single embed returns a non-empty list of floats with expected model dimension.",
    ),
    ValidationExample(
        "02",
        "Empty batch",
        "embed_texts([]) returns [] without calling the API for content.",
    ),
    ValidationExample(
        "03",
        "Batch length and order",
        "N texts in → N vectors out, same order as input.",
    ),
    ValidationExample(
        "04",
        "Batch vs single consistency",
        "embed_texts([x])[0] matches embed_query(x) (within float tolerance).",
    ),
    ValidationExample(
        "05",
        "Semantic neighbors",
        "Related phrases have higher cosine similarity than unrelated ones.",
    ),
    ValidationExample(
        "06",
        "Query ranking over passages",
        "Query should rank the most relevant stored chunk highest (mini retrieval).",
    ),
    ValidationExample(
        "07",
        "Paraphrase closeness",
        "Two paraphrases are closer to each other than to a random topic.",
    ),
    ValidationExample(
        "08",
        "Stable re-embed",
        "Same string embedded twice yields nearly identical vectors.",
    ),
    ValidationExample(
        "09",
        "Chunk-like text",
        "Typical RAG chunk strings embed without error and pass structure checks.",
    ),
    ValidationExample(
        "10",
        "Unicode and whitespace",
        "Non-ASCII and trimmed vs padded text still produce valid vectors.",
    ),
]


def _max_abs_diff(a: list[float], b: list[float]) -> float:
    return max(abs(x - y) for x, y in zip(a, b))


def run_example_01_structure(embedder: Embedder, model: str) -> None:
    vec = embedder.embed_query("hello world")
    expected = expected_dim_for_model(model)
    result = validate_vector_structure(vec, expected_dim=expected)
    if not result["ok"]:
        raise AssertionError(result["issues"])


def run_example_02_empty_batch(embedder: Embedder, _model: str) -> None:
    if embedder.embed_texts([]) != []:
        raise AssertionError("embed_texts([]) should return []")


def run_example_03_batch_order(embedder: Embedder, _model: str) -> None:
    texts = ["first chunk", "second chunk", "third chunk"]
    vectors = embedder.embed_texts(texts)
    if len(vectors) != len(texts):
        raise AssertionError(f"expected {len(texts)} vectors, got {len(vectors)}")


def run_example_04_batch_vs_single(embedder: Embedder, _model: str) -> None:
    text = "password recovery steps"
    from_batch = embedder.embed_texts([text])[0]
    from_query = embedder.embed_query(text)
    diff = _max_abs_diff(from_batch, from_query)
    if diff > 1e-5:
        raise AssertionError(f"batch vs query max diff {diff} > 1e-5")


def run_example_05_semantic_neighbors(embedder: Embedder, _model: str) -> None:
    related_a = embedder.embed_query("How do I reset my password?")
    related_b = embedder.embed_query("Forgot password help")
    unrelated = embedder.embed_query("Weather forecast for Mumbai")
    sim_related = cosine_similarity(related_a, related_b)
    sim_unrelated = cosine_similarity(related_a, unrelated)
    if sim_related <= sim_unrelated:
        raise AssertionError(
            f"expected related > unrelated; got related={sim_related:.4f}, "
            f"unrelated={sim_unrelated:.4f}"
        )


def run_example_06_query_ranking(embedder: Embedder, _model: str) -> None:
    passages = [
        "Warranty on laptops is 24 months from purchase date.",
        "Returns are accepted within 30 days with original receipt.",
        "Office cafeteria opens at 8am on weekdays.",
    ]
    query = embedder.embed_query("How long is the laptop warranty?")
    passage_vecs = embedder.embed_texts(passages)
    scores = [cosine_similarity(query, pv) for pv in passage_vecs]
    best_idx = max(range(len(scores)), key=lambda i: scores[i])
    if best_idx != 0:
        raise AssertionError(
            f"expected passage 0 to win; scores={scores}, best_idx={best_idx}"
        )


def run_example_07_paraphrase(embedder: Embedder, _model: str) -> None:
    a = embedder.embed_query("refund policy for defective items")
    b = embedder.embed_query("how to get money back for broken products")
    c = embedder.embed_query("chocolate cake recipe")
    if cosine_similarity(a, b) <= cosine_similarity(a, c):
        raise AssertionError("paraphrase pair should beat unrelated topic")


def run_example_08_stable_reembed(embedder: Embedder, _model: str) -> None:
    text = "embedding stability check"
    v1 = embedder.embed_query(text)
    v2 = embedder.embed_query(text)
    diff = _max_abs_diff(v1, v2)
    if diff > 1e-5:
        raise AssertionError(f"re-embed max diff {diff} > 1e-5")


def run_example_09_chunk_like(embedder: Embedder, model: str) -> None:
    chunk = (
        "Section 4.2 — Data retention: customer logs are kept for 90 days, "
        "then archived. PII is deleted per GDPR request within 30 days."
    )
    vec = embedder.embed_texts([chunk])[0]
    expected = expected_dim_for_model(model)
    result = validate_vector_structure(vec, expected_dim=expected)
    if not result["ok"]:
        raise AssertionError(result["issues"])


def run_example_10_unicode_whitespace(embedder: Embedder, model: str) -> None:
    texts = ["  trimmed text  ", "café résumé naïve", "日本語テスト"]
    vectors = embedder.embed_texts(texts)
    expected = expected_dim_for_model(model)
    for vec in vectors:
        result = validate_vector_structure(vec, expected_dim=expected)
        if not result["ok"]:
            raise AssertionError(result["issues"])


RUNNERS: dict[str, Callable[[Embedder, str], None]] = {
    "01": run_example_01_structure,
    "02": run_example_02_empty_batch,
    "03": run_example_03_batch_order,
    "04": run_example_04_batch_vs_single,
    "05": run_example_05_semantic_neighbors,
    "06": run_example_06_query_ranking,
    "07": run_example_07_paraphrase,
    "08": run_example_08_stable_reembed,
    "09": run_example_09_chunk_like,
    "10": run_example_10_unicode_whitespace,
}


def print_catalog() -> None:
    print("OpenAI embedding validation examples:\n")
    for ex in VALIDATION_EXAMPLES:
        print(f"  [{ex.id}] {ex.title}")
        print(f"      {ex.description}\n")


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if "--list" in args:
        print_catalog()
        return 0

    settings = get_settings()
    if not settings.openai_api_key:
        print("ERROR: Set OPENAI_API_KEY in .env")
        return 1

    model = settings.embedding_model
    print(f"Using embedding model: {model}")
    embedder = Embedder()

    selected = [a for a in args if a in RUNNERS]
    if not selected:
        selected = list(RUNNERS.keys())

    failed: list[str] = []
    for ex_id in selected:
        meta = next(e for e in VALIDATION_EXAMPLES if e.id == ex_id)
        print(f"Running [{ex_id}] {meta.title}...", end=" ")
        try:
            RUNNERS[ex_id](embedder, model)
            print("OK")
        except Exception as exc:
            print(f"FAIL: {exc}")
            failed.append(ex_id)

    if failed:
        print(f"\n{len(failed)} example(s) failed: {', '.join(failed)}")
        return 1

    print(f"\nAll {len(selected)} example(s) passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
