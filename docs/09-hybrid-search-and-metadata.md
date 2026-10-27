# Hybrid search and metadata filters

## Why hybrid?

| Method | Good at | Weak at |
|--------|---------|---------|
| **Vector** | Paraphrases, concepts | Exact codes (`SEV-1`, SKU, law cite) |
| **BM25 (lexical)** | Rare tokens, acronyms | Synonyms and rephrasing |

**Enterprise default:** retrieve 20–50 with both, **fuse** with RRF, then **rerank** to top-k.

## Code in this project

| Piece | File |
|-------|------|
| BM25 index | `src/rag/step05_retrieve/bm25_index.py` |
| RRF fusion | same file + `hybrid_search.py` |
| Persisted lexical index | `data/processed/bm25_index.json` (updated on index) |
| Demo script | `python -m src.rag.step05_retrieve.validate_hybrid_search` |

## Enable hybrid in the API pipeline

```env
RETRIEVAL_MODE=hybrid
USE_QUERY_TRANSFORM=true
```

Flow:

1. `transform_query()` expands acronyms (VPN, SLA, PII…).
2. Vector search in Chroma.
3. BM25 search in lexical index.
4. RRF merge → optional lexical rerank (`RERANK_MODE`).

## Metadata filtering (multi-tenant / department)

Chroma supports `where` filters. Example schema: `data/examples/metadata/chunk_metadata_schema.json`.

```python
from src.rag.step05_retrieve.retriever import Retriever

retriever = Retriever()
hits = retriever.retrieve(
    "VPN provisioning time",
    metadata_filter={"department": "it"},
)
```

**Practice:** when indexing, add `department`, `classification` to each chunk’s metadata in `pipeline.py` (extend `metadatas.append(...)`).

## Parent–child retrieval

1. Embed **children** (small, precise).
2. On hit, load **parent** text for the LLM (wider context).

Implementation: `src/rag/step02_chunk/parent_child.py` — Lab 2 in [11-hands-on-labs.md](11-hands-on-labs.md).

Next: [10-governance-security.md](10-governance-security.md).
