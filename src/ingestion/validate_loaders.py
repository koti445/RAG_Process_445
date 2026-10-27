"""
Smoke-test loaders on files under data/examples/ (no network).

    python -m src.ingestion.validate_loaders
"""

from __future__ import annotations

from pathlib import Path

from src.core.config import get_settings
from src.ingestion.loaders.email_loader import EmailLoader
from src.ingestion.loaders.file_loader import FileLoader


def _preview(text: str, limit: int = 120) -> str:
    one_line = " ".join(text.split())
    return one_line[:limit] + ("..." if len(one_line) > limit else "")


def main() -> None:
    base = get_settings().base_dir / "data" / "examples"
    file_loader = FileLoader()
    email_loader = EmailLoader()

    md_path = base / "corpus" / "acme_support_faq.md"
    docs = file_loader.load(str(md_path))
    print(f"[file] {md_path.name}: {len(docs)} doc(s)")
    print(f"       preview: {_preview(docs[0].content)}\n")

    eml_path = base / "emails" / "order_confirmation.eml"
    emails = email_loader.load(str(eml_path))
    print(f"[email] {eml_path.name}: subject={emails[0].metadata.get('subject')}")
    print(f"        preview: {_preview(emails[0].content)}\n")

    print("Other loaders (URL, image OCR, video, zip) are registered in src/ingestion/registry.py.")
    print("See docs/02-ingestion.md for how to test each type safely.")


if __name__ == "__main__":
    main()
