# RAG Process 445 — learn-by-doing RAG

A step-by-step **Retrieval-Augmented Generation** project with ingestion, chunking, embeddings, Chroma vector search, reranking, generation, and evaluation (offline + optional **RAGAS** / **DeepEval**).

**New here?** Follow [docs/00-learning-path.md](docs/00-learning-path.md), then [docs/01-beginners-guide.md](docs/01-beginners-guide.md).

**Setup and validation:** [docs/13-configuration-execution-validation.md](docs/13-configuration-execution-validation.md)

## What is included

- **Data types:** text, markdown, PDF, DOCX, email (`.eml`), URL, image OCR, zip, video hooks
- **Chunking:** token, sentence, paragraph, recursive (`CHUNK_STRATEGY`)
- **Embeddings:** OpenAI (`validate_embedding` examples)
- **Vector DB:** Chroma + Postgres metadata
- **Reranking:** none, lexical, optional cross-encoder (`RERANK_MODE`)
- **Hybrid retrieval:** BM25 + vector with RRF (`RETRIEVAL_MODE=hybrid`)
- **Query transform:** acronym expansion for enterprise terms (`USE_QUERY_TRANSFORM`)
- **Parent–child chunking:** `src/rag/step02_chunk/parent_child.py`
- **Enterprise corpora:** HR policy + IT runbook under `data/examples/corpus/`
- **Hands-on labs:** `python -m src.rag.practice.run_labs`
- **Mock practice data:** `data/examples/`
- **Tests:** `pytest tests`

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Edit .env — set OPENAI_API_KEY when using embed/generate/eval LLM tools

python -m src.ingestion.validate_loaders
python -m src.rag.step02_chunk.validate_chunking
python -m src.rag.step08_evaluate.run_practice_eval --mode offline --mock-retrieval
python -m pytest tests -q
```

## Documentation map

Full index: [docs/README.md](docs/README.md)

## Optional evaluation dependencies

```powershell
pip install -r requirements-eval.txt
python -m src.rag.step08_evaluate.run_practice_eval --framework ragas
```

## API (Docker)

See `docker-compose.yml` for Postgres. Run migrations with Alembic, then start the FastAPI app from `src/main.py`.

## Project layout

```
src/ingestion/          # loaders per source type
src/rag/step02_chunk/   # chunking + validate_chunking.py
src/rag/step03_embed/   # OpenAI embeddings
src/rag/step04_store/   # Chroma
src/rag/step05_retrieve/# retrieval + reranker
src/rag/step06_generate/
src/rag/step07_pipeline/
src/rag/step08_evaluate/ # metrics, RAGAS, DeepEval, CLI
data/examples/           # ACME mock corpus + eval JSON
docs/                    # beginner-friendly guides
```
