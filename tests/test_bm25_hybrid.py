from src.rag.step05_retrieve.bm25_index import Bm25Index, reciprocal_rank_fusion
from src.rag.step05_retrieve.query_transform import transform_query


def test_bm25_ranks_keyword_match():
    index = Bm25Index()
    index.add_many(
        ["a", "b"],
        ["laptop warranty twenty four months", "shipping five to seven days"],
    )
    hits = index.search("laptop warranty", top_k=2)
    assert hits[0].doc_id == "a"


def test_rrf_combines_lists():
    fused = reciprocal_rank_fusion([["a", "b", "c"], ["b", "a"]])
    ids = [x[0] for x in fused]
    assert ids[0] in {"a", "b"}
    assert "c" in ids


def test_query_transform_expands_vpn():
    t = transform_query("Do I need VPN for CRM?")
    assert "virtual private network" in t.rewritten.lower()
