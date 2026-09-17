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
    Simple keyword-based evaluator for practice.
    Later you can replace this with RAGAS or LLM-as-judge.
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
        top_k = retrieved_ids[:k]
        if not top_k:
            return 0.0
        hits = sum(1 for item_id in top_k if item_id in relevant_ids)
        return hits / len(top_k)