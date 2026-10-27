"""Chunk helpers that do not need tiktoken (offline / locked-down networks)."""

from __future__ import annotations

import re


def split_markdown_sections(text: str) -> list[str]:
    """Split on ## headings and blank lines — good for enterprise policy/runbook files."""
    parts = re.split(r"\n##\s+", text)
    chunks: list[str] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if not part.startswith("#"):
            part = "## " + part
        chunks.append(part)
    return chunks
