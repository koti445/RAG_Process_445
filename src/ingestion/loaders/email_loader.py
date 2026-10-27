"""Extract plain text from .eml email files."""

from __future__ import annotations

import email
from email import policy
from pathlib import Path

from src.domain.models import LoadedDocument
from src.ingestion.base import BaseLoader


class EmailLoader(BaseLoader):
    SUPPORTED = {".eml", ".msg"}

    def supports(self, source_type: str) -> bool:
        return source_type == "email"

    def load(self, source: str, **kwargs) -> list[LoadedDocument]:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"Email file not found: {source}")

        suffix = path.suffix.lower()
        if suffix != ".eml":
            raise ValueError(
                f"Only .eml is supported in this project (got {suffix}). "
                "Convert Outlook .msg to .eml or use a dedicated parser."
            )

        raw = path.read_bytes()
        message = email.message_from_bytes(raw, policy=policy.default)

        subject = str(message.get("subject", ""))
        from_addr = str(message.get("from", ""))
        to_addr = str(message.get("to", ""))
        date = str(message.get("date", ""))

        body_parts: list[str] = []
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_content()
                    if isinstance(payload, str) and payload.strip():
                        body_parts.append(payload.strip())
        else:
            payload = message.get_content()
            if isinstance(payload, str):
                body_parts.append(payload.strip())

        body = "\n\n".join(body_parts) if body_parts else ""
        header_block = (
            f"Subject: {subject}\nFrom: {from_addr}\nTo: {to_addr}\nDate: {date}\n"
        )
        content = f"{header_block}\n{body}".strip()

        return [
            LoadedDocument(
                content=content,
                source_type="email",
                source_uri=str(path),
                metadata={
                    "file_type": "eml",
                    "subject": subject,
                    "from": from_addr,
                    "to": to_addr,
                },
            )
        ]
