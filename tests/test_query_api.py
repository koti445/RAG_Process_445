import pytest


@pytest.mark.skip(reason="Requires indexed documents and OpenAI")
def test_query_endpoint(client):
    response = client.post(
        "/api/v1/query/",
        json={"question": "What is RAG?"},
    )
    assert response.status_code == 200