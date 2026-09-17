def test_ingest_invalid_source(client):
    response = client.post(
        "/api/v1/ingest/",
        json={"source_type": "file", "source_uri": "missing.txt"},
    )
    assert response.status_code == 400