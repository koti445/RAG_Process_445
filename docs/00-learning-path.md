# Learning path: basic → enterprise

Use this as a **curriculum**. Each level builds on the previous one.

## Level 0 — Concepts (1–2 hours)

| Goal | Resource |
|------|----------|
| What RAG is | [01-beginners-guide.md](01-beginners-guide.md) |
| Terms (embedding, top-k, hallucination) | [12-glossary.md](12-glossary.md) |

## Level 1 — Run the pipeline (half day)

| Goal | Action |
|------|--------|
| Load sample files | `python -m src.ingestion.validate_loaders` |
| Compare chunk strategies | `python -m src.rag.step02_chunk.validate_chunking` |
| Score mock Q&A | `python -m src.rag.step08_evaluate.run_practice_eval --mode offline --mock-retrieval` |
| Unit tests (no API) | `python -m pytest tests/test_bm25_hybrid.py tests/test_email_loader.py -q` |

## Level 2 — Retrieval quality (1 day)

| Topic | Resource / command |
|-------|------------------|
| Lexical + vector (hybrid) | [09-hybrid-search-and-metadata.md](09-hybrid-search-and-metadata.md), `python -m src.rag.step05_retrieve.validate_hybrid_search` |
| Reranking | [05-retrieval-reranking.md](05-retrieval-reranking.md), `RERANK_MODE=lexical` |
| Query prep | `src/rag/step05_retrieve/query_transform.py`, Lab 4 in [11-hands-on-labs.md](11-hands-on-labs.md) |
| Parent–child chunks | `src/rag/step02_chunk/parent_child.py`, Lab 2 |

## Level 3 — Enterprise patterns (2–3 days)

| Topic | Resource |
|-------|----------|
| Reference architecture | [08-enterprise-architecture.md](08-enterprise-architecture.md) |
| Security & governance | [10-governance-security.md](10-governance-security.md) |
| Metadata filters | [09-hybrid-search-and-metadata.md](09-hybrid-search-and-metadata.md), `data/examples/metadata/chunk_metadata_schema.json` |
| Practice corpora | `data/examples/corpus/enterprise_*.md` |
| Guided labs | `python -m src.rag.practice.run_labs` |

## Level 4 — Measure and ship (ongoing)

| Topic | Resource |
|-------|----------|
| Offline + RAGAS + DeepEval | [06-evaluation.md](06-evaluation.md) |
| What breaks in prod | [07-step-criticality.md](07-step-criticality.md) |
| Prometheus metrics | `src/metrics/prometheus.py`, `/metrics` route |

## What this repo teaches vs what you add in real companies

| Taught here | Usually added at scale |
|-------------|-------------------------|
| Chroma + Postgres | Managed vector DB, multi-region |
| OpenAI embed + chat | Azure OpenAI, private models, routing |
| BM25 + RRF hybrid | Elasticsearch / Azure AI Search hybrid |
| Keyword + RAGAS eval | Human review, A/B tests, guardrails |
| Single tenant API | Per-tenant collections, ACL on metadata |

Nothing on this list blocks learning—the patterns are the same; only the infrastructure grows.
