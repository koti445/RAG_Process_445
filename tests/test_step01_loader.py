from src.ingestion.loaders.file_loader import FileLoader


def test_load_txt(tmp_path):
    sample = tmp_path / "sample.txt"
    sample.write_text("Hello RAG world", encoding="utf-8")

    loader = FileLoader()
    docs = loader.load(str(sample))

    assert len(docs) == 1
    assert "Hello RAG" in docs[0].content
    assert docs[0].metadata["file_type"] == "txt"