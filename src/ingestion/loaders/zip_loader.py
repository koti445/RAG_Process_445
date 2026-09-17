import tempfile
import zipfile
from pathlib import Path

from src.domain.models import LoadedDocument
from src.ingestion.base import BaseLoader
from src.ingestion.loaders.file_loader import FileLoader


class ZipLoader(BaseLoader):
    def supports(self, source_type: str) -> bool:
        return source_type == "zip"

    def load(self, source: str, **kwargs) -> list[LoadedDocument]:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"ZIP file not found: {source}")

        file_loader = FileLoader()
        all_docs: list[LoadedDocument] = []

        with zipfile.ZipFile(path, "r") as zf, tempfile.TemporaryDirectory() as tmp:
            zf.extractall(tmp)
            for extracted in Path(tmp).rglob("*"):
                if extracted.is_file() and extracted.suffix.lower() in FileLoader.SUPPORTED:
                    docs = file_loader.load(str(extracted))
                    for doc in docs:
                        doc.metadata["archive"] = str(path)
                        doc.metadata["inner_path"] = extracted.name
                    all_docs.extend(docs)

        return all_docs