from pathlib import Path

from src.ingestion.loaders.email_loader import EmailLoader


def test_load_eml_example():
    base = Path(__file__).resolve().parent.parent / "data" / "examples" / "emails"
    path = base / "order_confirmation.eml"
    loader = EmailLoader()
    docs = loader.load(str(path))
    assert len(docs) == 1
    assert "order number 445" in docs[0].content.lower()
    assert docs[0].metadata["subject"]
