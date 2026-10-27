"""
RAGAS evaluation (optional).

Install: pip install -r requirements-eval.txt
Requires: OPENAI_API_KEY (RAGAS uses an LLM for some metrics).

Run:
    python -m src.rag.step08_evaluate.run_practice_eval --framework ragas
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.rag.step08_evaluate.practice_dataset import EvalSample


@dataclass
class RagasRunResult:
    metrics: dict[str, float]
    raw: Any


def run_ragas_on_samples(
    samples: list[EvalSample],
    answers: list[str],
) -> RagasRunResult:
    try:
        from datasets import Dataset
        from ragas import evaluate
        from ragas.metrics import answer_relevancy, context_precision, faithfulness
    except ImportError as exc:
        raise ImportError(
            "RAGAS not installed. Run: pip install -r requirements-eval.txt"
        ) from exc

    if len(samples) != len(answers):
        raise ValueError("samples and answers must have the same length")

    rows = {
        "question": [s.question for s in samples],
        "answer": answers,
        "contexts": [s.contexts for s in samples],
        "ground_truth": [s.ground_truth for s in samples],
    }
    dataset = Dataset.from_dict(rows)
    result = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision],
    )
    metrics = {k: float(v) for k, v in result.items()}
    return RagasRunResult(metrics=metrics, raw=result)
