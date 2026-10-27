# Steps 3–4 — Embeddings and vector store

## Embeddings (step 3)

**Idea:** Similar meanings → similar lists of numbers (vectors).

- Code: `src/rag/step03_embed/embedder.py` (OpenAI)
- Helpers: `embedding_utils.py`
- Practice validation (needs `OPENAI_API_KEY`):

```powershell
python -m src.rag.step03_embed.validate_embedding
python -m src.rag.step03_embed.validate_embedding 01 06
```

## Vector database (step 4)

This project uses **Chroma** locally (`CHROMA_PERSIST_DIR`).

| Concept | In this repo |
|---------|----------------|
| Collection | `rag_chunks` in `VectorStore` |
| Vector ID | Same as chunk UUID in Postgres |
| Document text | Stored in Chroma for retrieval display |
| Metadata | `document_id`, etc. |

Postgres (`chunks` table) is the **system of record**; Chroma is the **similarity search engine**.

### Other vector DBs (learning note)

The same pattern works for Pinecone, Weaviate, Qdrant, pgvector: **upsert (id, vector, text, metadata)** then **query by vector**.

## Criticality

| Severity | If embedding/index fails… |
|----------|---------------------------|
| Critical | Retrieval returns random or empty context → hallucinations. |
| High | Dimension mismatch (wrong model) breaks search entirely. |

Next: [05-retrieval-reranking.md](05-retrieval-reranking.md).
