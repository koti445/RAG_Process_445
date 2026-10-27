"""
Query preparation patterns used in production RAG.

This module uses **deterministic** transforms for offline labs (no API).
Optional LLM rewrite can be added later with the same interface.
"""

from __future__ import annotations

from dataclasses import dataclass

# Enterprise acronym expansions (practice only — tune per domain)
_ACRONYM_MAP = {
    "sla": "service level agreement SLA",
    "pii": "personally identifiable information PII",
    "sso": "single sign-on SSO",
    "vpn": "virtual private network VPN",
    "rbac": "role based access control RBAC",
}


@dataclass
class TransformedQuery:
    original: str
    rewritten: str
    variants: list[str]
    notes: list[str]


def expand_acronyms(question: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    lower = question.lower()
    extra_terms: list[str] = []
    for key, expansion in _ACRONYM_MAP.items():
        if key in lower.split() or f" {key}" in lower or f"{key} " in lower:
            extra_terms.append(expansion)
            notes.append(f"expanded:{key}")
    if not extra_terms:
        return question, notes
    return f"{question} ({'; '.join(extra_terms)})", notes


def generate_subqueries(question: str) -> list[str]:
    """Simple multi-query: original + keyword-focused variant."""
    base, _ = expand_acronyms(question)
    variants = [question.strip(), base.strip()]
    if "?" in question:
        variants.append(question.replace("?", "").strip())
    # dedupe preserving order
    seen: set[str] = set()
    out: list[str] = []
    for v in variants:
        if v and v not in seen:
            seen.add(v)
            out.append(v)
    return out


def transform_query(question: str) -> TransformedQuery:
    rewritten, notes = expand_acronyms(question)
    variants = generate_subqueries(question)
    return TransformedQuery(
        original=question,
        rewritten=rewritten,
        variants=variants,
        notes=notes,
    )
