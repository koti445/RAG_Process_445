# RAG learning docs (start here)

**Curriculum:** [00-learning-path.md](00-learning-path.md) (basic → enterprise)

Read in this order:

| # | Document | Who it is for |
|---|----------|----------------|
| 0 | [00-learning-path.md](00-learning-path.md) | Structured curriculum |
| 1 | [01-beginners-guide.md](01-beginners-guide.md) | Anyone new — explained like a story |
| 2 | [02-ingestion.md](02-ingestion.md) | PDF, DOCX, email, URL, images, zip, video |
| 3 | [03-chunking.md](03-chunking.md) | All chunk strategies + validation |
| 4 | [04-embedding-and-index.md](04-embedding-and-index.md) | Embeddings, Chroma, Postgres metadata |
| 5 | [05-retrieval-reranking.md](05-retrieval-reranking.md) | Search, top-k, rerankers |
| 6 | [06-evaluation.md](06-evaluation.md) | Offline metrics, RAGAS, DeepEval |
| 7 | [07-step-criticality.md](07-step-criticality.md) | What breaks the pipeline if wrong |
| 8 | [08-enterprise-architecture.md](08-enterprise-architecture.md) | Production reference diagram |
| 9 | [09-hybrid-search-and-metadata.md](09-hybrid-search-and-metadata.md) | BM25, RRF, filters |
| 10 | [10-governance-security.md](10-governance-security.md) | PII, audit, safe answers |
| 11 | [11-hands-on-labs.md](11-hands-on-labs.md) | Six guided labs |
| 12 | [12-glossary.md](12-glossary.md) | Simple definitions |
| 13 | [13-configuration-execution-validation.md](13-configuration-execution-validation.md) | **Setup, `.env`, run & validate each step** |

## Quick practice commands

```powershell
cd c:\Learning\RAG\RAG_Process_445
python -m src.ingestion.validate_loaders
python -m src.rag.step02_chunk.validate_chunking
python -m src.rag.step08_evaluate.run_practice_eval --mode offline --mock-retrieval
python -m src.rag.step05_retrieve.validate_hybrid_search
python -m src.rag.practice.run_labs
python -m pytest tests -q
```

With OpenAI key in `.env`:

```powershell
python -m src.rag.step03_embed.validate_embedding
```

Optional evaluation frameworks:

```powershell
pip install -r requirements-eval.txt
python -m src.rag.step08_evaluate.run_practice_eval --framework ragas
python -m src.rag.step08_evaluate.run_practice_eval --framework deepeval
```
