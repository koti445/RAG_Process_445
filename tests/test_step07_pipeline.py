import pytest


@pytest.mark.skip(reason="Requires PostgreSQL, OpenAI, and Chroma setup")
def test_pipeline_index_and_query():
    pass