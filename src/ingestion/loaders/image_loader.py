from pathlib import Path

import pytesseract
from PIL import Image

from src.core.config import get_settings
from src.domain.models import LoadedDocument
from src.ingestion.base import BaseLoader


class ImageLoader(BaseLoader):
    SUPPORTED = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}

    def supports(self, source_type: str) -> bool:
        return source_type == "image"

    def load(self, source: str, **kwargs) -> list[LoadedDocument]:
        settings = get_settings()
        if settings.tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {source}")

        image = Image.open(path)
        text = pytesseract.image_to_string(image)

        return [
            LoadedDocument(
                content=text.strip(),
                source_type="image",
                source_uri=str(path),
                metadata={"file_type": path.suffix.lstrip("."), "ocr": True},
            )
        ]