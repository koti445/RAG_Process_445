from src.rag.step08_evaluate.run_practice_eval import run_offline


def test_offline_eval_runs_on_mock_data():
    report = run_offline(mock_retrieval=True)
    assert report["sample_count"] >= 3
    assert report["keyword_hit_rate"] == 1.0
    assert len(report["retrieval"]) == report["sample_count"]
