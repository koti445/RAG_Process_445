from src.rag.step08_evaluate.retrieval_metrics import compute_retrieval_metrics


def test_perfect_retrieval():
    retrieved = ["a", "b", "c"]
    relevant = {"a"}
    m = compute_retrieval_metrics(retrieved, relevant, k=3)
    assert m.precision_at_k == 1 / 3
    assert m.mrr == 1.0
    assert m.hit_at_k is True


def test_miss_retrieval():
    retrieved = ["x", "y"]
    relevant = {"a"}
    m = compute_retrieval_metrics(retrieved, relevant, k=2)
    assert m.mrr == 0.0
    assert m.hit_at_k is False
