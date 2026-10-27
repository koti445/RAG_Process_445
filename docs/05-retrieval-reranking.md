# Step 5 — Retrieval and reranking

## Retrieval

1. Embed the user question.
2. Ask Chroma for **top-k** nearest chunks (`TOP_K` in `.env`).
3. Convert distance to a simple score (`1 - distance`).

Code: `src/rag/step05_retrieve/retriever.py`

## Hybrid search (enterprise)

Vector-only search can miss exact tokens like `SEV-1` or `ServiceNow`. Enable:

```env
RETRIEVAL_MODE=hybrid
```

Details: [09-hybrid-search-and-metadata.md](09-hybrid-search-and-metadata.md)

Practice:

```powershell
python -m src.rag.step05_retrieve.validate_hybrid_search
```

## Reranking (optional but important in production)

First pass (vector search) is fast but not perfect. Reranking reorders candidates.

| Mode | `.env` value | Needs extra install |
|------|--------------|---------------------|
| None | `RERANK_MODE=none` | No |
| Lexical boost | `RERANK_MODE=lexical` | No — great for practice |
| Cross-encoder | `RERANK_MODE=cross_encoder` | `pip install sentence-transformers` |

```env
RERANK_MODE=lexical
```

## Practice test

```powershell
python -m pytest tests/test_reranker.py -q
```

## Criticality

| Severity | If retrieval is weak… |
|----------|------------------------|
| Critical | Right answer never reaches the LLM. |
| Medium | Without rerank, right chunk may be rank 4–10 and get truncated. |

Next: [06-evaluation.md](06-evaluation.md).
