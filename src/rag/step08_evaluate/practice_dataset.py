"""Load mock evaluation sets from data/examples/eval/."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from src.core.config import get_settings


@dataclass
class EvalSample:
    id: str
    question: str
    ground_truth: str
    expected_keywords: list[str]
    relevant_chunk_ids: list[str]
    contexts: list[str]


def default_eval_path() -> Path:
    return get_settings().base_dir / "data" / "examples" / "eval" / "eval_dataset.json"


def load_eval_dataset(path: Path | None = None) -> list[EvalSample]:
    path = path or default_eval_path()
    if not path.exists():
        raise FileNotFoundError(f"Eval dataset not found: {path}")

    raw = json.loads(path.read_text(encoding="utf-8"))
    samples: list[EvalSample] = []
    for row in raw.get("samples", []):
        samples.append(
            EvalSample(
                id=row["id"],
                question=row["question"],
                ground_truth=row.get("ground_truth", ""),
                expected_keywords=row.get("expected_keywords", []),
                relevant_chunk_ids=row.get("relevant_chunk_ids", []),
                contexts=row.get("contexts", []),
            )
        )
    return samples
