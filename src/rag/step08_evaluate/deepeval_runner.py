"""
DeepEval evaluation (optional).

Install: pip install -r requirements-eval.txt
Requires: OPENAI_API_KEY for LLM-based metrics.

Run:
    python -m src.rag.step08_evaluate.run_practice_eval --framework deepeval
"""

from __future__ import annotations

from dataclasses import dataclass

from src.rag.step08_evaluate.practice_dataset import EvalSample


@dataclass
class DeepEvalRunResult:
    average_score: float
    per_sample: list[dict[str, float | str]]


def run_deepeval_on_samples(
    samples: list[EvalSample],
    answers: list[str],
) -> DeepEvalRunResult:
    try:
        from deepeval.metrics import AnswerRelevancyMetric
        from deepeval.test_case import LLMTestCase
    except ImportError as exc:
        raise ImportError(
            "DeepEval not installed. Run: pip install -r requirements-eval.txt"
        ) from exc

    if len(samples) != len(answers):
        raise ValueError("samples and answers must have the same length")

    metric = AnswerRelevancyMetric(threshold=0.5)
    per_sample: list[dict[str, float | str]] = []
    scores: list[float] = []

    for sample, answer in zip(samples, answers):
        context = "\n".join(sample.contexts)
        test_case = LLMTestCase(
            input=sample.question,
            actual_output=answer,
            retrieval_context=[context] if context else [],
            expected_output=sample.ground_truth or None,
        )
        metric.measure(test_case)
        score = float(metric.score or 0.0)
        scores.append(score)
        per_sample.append(
            {
                "id": sample.id,
                "answer_relevancy": score,
                "reason": str(metric.reason or ""),
            }
        )

    avg = sum(scores) / len(scores) if scores else 0.0
    return DeepEvalRunResult(average_score=avg, per_sample=per_sample)
