import httpx
from bs4 import BeautifulSoup

from src.core.config import get_settings
from src.domain.models import LoadedDocument
from src.ingestion.base import BaseLoader


class UrlLoader(BaseLoader):
    def supports(self, source_type: str) -> bool:
        return source_type in {"url", "page"}

    def load(self, source: str, **kwargs) -> list[LoadedDocument]:
        settings = get_settings()

        with httpx.Client(timeout=settings.request_timeout_seconds) as client:
            response = client.get(source)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        title = soup.title.string.strip() if soup.title and soup.title.string else source

        return [
            LoadedDocument(
                content=text,
                source_type="url",
                source_uri=source,
                metadata={"title": title, "status_code": response.status_code},
            )
        ]