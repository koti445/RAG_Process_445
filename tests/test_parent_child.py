from src.rag.step02_chunk.parent_child import ParentChildChunker


def test_parent_child_produces_more_children_than_parents():
    text = ("Section one. " * 30 + "\n\n" + "Section two. " * 30) * 5
    bundle = ParentChildChunker(parent_chunk_size=400, child_chunk_size=120).chunk(text)
    assert len(bundle.children) >= len(bundle.parents)
    assert bundle.children[0].metadata.get("parent_id")
