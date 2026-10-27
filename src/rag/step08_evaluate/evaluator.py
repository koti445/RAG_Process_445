from dataclasses import dataclass


@dataclass
class EvalResult:
    question: str
    expected_keywords: list[str]
    answer: str
    hit: bool
    matched_keywords: list[str]


class RAGEvaluator:
    """
    Simple keyword-based evaluator for practice (no API cost).

    For full pipeline scoring see:
    - python -m src.rag.step08_evaluate.run_practice_eval --mode offline
    - RAGAS / DeepEval via --framework (optional deps)
    """

    def evaluate_answer(
        self,
        question: str,
        answer: str,
        expected_keywords: list[str],
    ) -> EvalResult:
        answer_lower = answer.lower()
        matched = [kw for kw in expected_keywords if kw.lower() in answer_lower]

        return EvalResult(
            question=question,
            expected_keywords=expected_keywords,
            answer=answer,
            hit=len(matched) > 0,
            matched_keywords=matched,
        )

    def precision_at_k(self, retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float:
        from src.rag.step08_evaluate.retrieval_metrics import precision_at_k

        return precision_at_k(retrieved_ids, relevant_ids, k)