"""
Practice evaluation CLI — works offline (keyword + retrieval) or with RAGAS / DeepEval.

Examples:
    python -m src.rag.step08_evaluate.run_practice_eval --mode offline
    python -m src.rag.step08_evaluate.run_practice_eval --mode offline --mock-retrieval
    python -m src.rag.step08_evaluate.run_practice_eval --framework ragas
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.rag.step08_evaluate.evaluator import RAGEvaluator
from src.rag.step08_evaluate.practice_dataset import load_eval_dataset
from src.rag.step08_evaluate.retrieval_metrics import compute_retrieval_metrics


def _mock_answers(samples) -> list[str]:
    """Deterministic answers for offline demos (no OpenAI)."""
    answers: list[str] = []
    for sample in samples:
        if sample.ground_truth:
            answers.append(sample.ground_truth)
        elif sample.expected_keywords:
            answers.append(
                f"Based on the documents, the answer relates to: {', '.join(sample.expected_keywords)}."
            )
        else:
            answers.append("I could not find enough context to answer confidently.")
    return answers


def run_offline(mock_retrieval: bool) -> dict:
    evaluator = RAGEvaluator()
    samples = load_eval_dataset()
    answers = _mock_answers(samples)

    keyword_hits = 0
    retrieval_rows: list[dict] = []

    for sample, answer in zip(samples, answers):
        kw = evaluator.evaluate_answer(sample.question, answer, sample.expected_keywords)
        if kw.hit:
            keyword_hits += 1

        if mock_retrieval and sample.relevant_chunk_ids:
            retrieved = sample.relevant_chunk_ids + ["noise_chunk_1", "noise_chunk_2"]
            metrics = compute_retrieval_metrics(
                retrieved_ids=retrieved,
                relevant_ids=set(sample.relevant_chunk_ids),
                k=3,
            )
            retrieval_rows.append(
                {
                    "id": sample.id,
                    "precision@3": metrics.precision_at_k,
                    "recall@3": metrics.recall_at_k,
                    "mrr": metrics.mrr,
                    "ndcg@3": metrics.ndcg_at_k,
                    "hit@3": metrics.hit_at_k,
                }
            )

    report = {
        "mode": "offline",
        "sample_count": len(samples),
        "keyword_hit_rate": keyword_hits / len(samples) if samples else 0.0,
        "retrieval": retrieval_rows,
        "note": "Use --framework ragas or deepeval with OPENAI_API_KEY for LLM-judged metrics.",
    }
    return report


def run_framework(name: str) -> dict:
    samples = load_eval_dataset()
    answers = _mock_answers(samples)

    if name == "ragas":
        from src.rag.step08_evaluate.ragas_runner import run_ragas_on_samples

        result = run_ragas_on_samples(samples, answers)
        return {"framework": "ragas", "metrics": result.metrics}

    if name == "deepeval":
        from src.rag.step08_evaluate.deepeval_runner import run_deepeval_on_samples

        result = run_deepeval_on_samples(samples, answers)
        return {
            "framework": "deepeval",
            "average_answer_relevancy": result.average_score,
            "per_sample": result.per_sample,
        }

    raise ValueError(f"Unknown framework: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="RAG practice evaluation")
    parser.add_argument("--mode", choices=["offline"], default="offline")
    parser.add_argument("--mock-retrieval", action="store_true")
    parser.add_argument(
        "--framework",
        choices=["ragas", "deepeval"],
        help="Optional LLM-based evaluation (needs requirements-eval.txt + API key)",
    )
    parser.add_argument("--out", type=Path, help="Write JSON report to this path")
    args = parser.parse_args()

    if args.framework:
        report = run_framework(args.framework)
    else:
        report = run_offline(mock_retrieval=args.mock_retrieval)

    text = json.dumps(report, indent=2)
    print(text)
    if args.out:
        args.out.write_text(text, encoding="utf-8")
        print(f"Wrote report to {args.out}")


if __name__ == "__main__":
    main()
