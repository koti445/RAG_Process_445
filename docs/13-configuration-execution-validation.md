# Configuration, execution, and validation guide

This document is the **operational manual** for RAG_Process_445: how to configure the app, run each pipeline stage, and prove each stage works.

**Audience:** Anyone setting up the project on Windows (PowerShell commands below; adapt paths for macOS/Linux).

**Related docs:** Concepts → [00-learning-path.md](00-learning-path.md) · Labs → [11-hands-on-labs.md](11-hands-on-labs.md)

---

## 1. Prerequisites

| Requirement | Purpose | Check |
|-------------|---------|--------|
| Python **3.11+** | Runtime | `python --version` |
| Git | Clone repo | `git --version` |
| Docker Desktop (optional) | Postgres for API | `docker compose version` |
| OpenAI API key (optional for offline) | Embeddings + chat + RAGAS | Set in `.env` |
| Tesseract (optional) | Image OCR | Install + set `TESSERACT_CMD` |

---

## 2. One-time project setup

### 2.1 Clone and virtual environment

```powershell
cd c:\Learning\RAG\RAG_Process_445
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Optional evaluation frameworks (RAGAS / DeepEval):

```powershell
pip install -r requirements-eval.txt
```

Optional cross-encoder reranking:

```powershell
pip install sentence-transformers
```

### 2.2 Environment file

```powershell
copy .env.example .env
```

Edit `.env` with a text editor. **Never commit `.env`** (it contains secrets).

### 2.3 Database (for FastAPI + full pipeline)

`docker-compose.yml` starts Postgres with:

| Setting | Value |
|---------|--------|
| User | `postgres` |
| Password | `postgres` |
| Database | `rag_process_445` |
| Port | `5432` |

**Align `DATABASE_URL` in `.env` with Docker:**

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/rag_process_445
```

> `.env.example` shows `rag_user` / `rag_db` — that is a template only. If you use `docker compose up`, use the credentials above or change both Docker and `.env` together.

Start database:

```powershell
docker compose up -d
docker compose ps
```

Apply schema migrations:

```powershell
alembic upgrade head
```

### 2.4 Data directories (auto-created)

| Path | Purpose |
|------|---------|
| `data/raw/` | Uploaded files from API |
| `data/processed/` | BM25 index JSON, lab reports |
| `data/chroma/` | Chroma vector persistence (`CHROMA_PERSIST_DIR`) |
| `data/examples/` | Practice corpus, eval JSON, sample email |

---

## 3. Configuration reference

All settings are loaded from **environment variables** (and `.env`) via `src/core/config.py`. Names are **case-insensitive** in `.env` (Pydantic maps `CHUNK_SIZE` → `chunk_size`).

### 3.1 Application and API

| Variable | Default (code) | Description |
|----------|----------------|-------------|
| `APP_NAME` | RAG Process 445 | FastAPI title |
| `APP_ENV` | development | Environment label |
| `DEBUG` | true | FastAPI debug |
| `API_PREFIX` | `/api/v1` | Route prefix for ingest/query |

### 3.2 Database and storage

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+psycopg2://postgres:postgres@localhost:5432/rag_process_445` | SQLAlchemy URL |
| `CHROMA_PERSIST_DIR` | `./data/chroma` | On-disk Chroma data |

### 3.3 OpenAI (embeddings + generation)

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *(empty)* | Required for embed, generate, RAGAS/DeepEval |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model name |
| `LLM_MODEL` | `gpt-4o-mini` | Chat model for answers |

### 3.4 Chunking and retrieval

| Variable | Default | Allowed values / notes |
|----------|---------|------------------------|
| `CHUNK_SIZE` | `500` | Token window size (tiktoken) |
| `CHUNK_OVERLAP` | `50` | Overlap between token windows |
| `CHUNK_STRATEGY` | `token` | `token`, `sentence`, `paragraph`, `recursive` |
| `TOP_K` | `5` | Chunks returned to generator |
| `RETRIEVAL_MODE` | `vector` | `vector` or `hybrid` (BM25 + RRF) |
| `USE_QUERY_TRANSFORM` | `true` | Expand acronyms (VPN, SLA, PII…) before embed |
| `RERANK_MODE` | `none` | `none`, `lexical`, `cross_encoder` |
| `RERANK_CROSS_ENCODER_MODEL` | `cross-encoder/ms-marco-MiniLM-L-6-v2` | Used when `RERANK_MODE=cross_encoder` |

### 3.5 Ingestion limits

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_UPLOAD_MB` | `50` | Max upload size via API |
| `REQUEST_TIMEOUT_SECONDS` | `30` | HTTP timeout for URL loader |
| `TESSERACT_CMD` | *(empty)* | Full path to `tesseract.exe` on Windows if not on PATH |

---

## 4. Recommended configuration profiles

Copy one profile into `.env` (merge with your `OPENAI_API_KEY` and `DATABASE_URL`).

### Profile A — Offline learning (no API, no DB)

Use for loaders, hybrid BM25 demo, offline eval, labs.

```env
OPENAI_API_KEY=
RETRIEVAL_MODE=vector
RERANK_MODE=none
USE_QUERY_TRANSFORM=true
```

Run validations in **Section 5** (Phase 1 only).

### Profile B — Full local RAG (API + OpenAI)

```env
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/rag_process_445
CHUNK_STRATEGY=sentence
TOP_K=5
RETRIEVAL_MODE=hybrid
RERANK_MODE=lexical
USE_QUERY_TRANSFORM=true
```

Run **Phases 1–4** and API steps in **Section 6**.

### Profile C — Enterprise-style retrieval experiment

```env
CHUNK_STRATEGY=recursive
RETRIEVAL_MODE=hybrid
RERANK_MODE=lexical
USE_QUERY_TRANSFORM=true
TOP_K=8
```

Re-index documents after changing chunk or retrieval settings.

---

## 5. Validation by pipeline stage

Run from **repository root** with venv activated.

### Validation matrix

| Stage | Command | Needs API? | Needs DB? | Success looks like |
|-------|---------|------------|-----------|-------------------|
| Ingestion loaders | `python -m src.ingestion.validate_loaders` | No | No | Previews for FAQ `.md` and sample `.eml` |
| Chunking | `python -m src.rag.step02_chunk.validate_chunking` | No* | No | Table of chunk counts per strategy |
| Embeddings | `python -m src.rag.step03_embed.validate_embedding` | **Yes** | No | All selected examples print `OK` |
| Embedding catalog | `python -m src.rag.step03_embed.validate_embedding --list` | No | No | Lists examples 01–10 |
| Hybrid / BM25 | `python -m src.rag.step05_retrieve.validate_hybrid_search` | No | No | HR policy queries return sensible `hr_*` ids |
| Offline evaluation | `python -m src.rag.step08_evaluate.run_practice_eval --mode offline --mock-retrieval` | No | No | JSON with `keyword_hit_rate`, `retrieval` array |
| Guided labs | `python -m src.rag.practice.run_labs` | No** | No | Labs 1–5 complete (Lab 2 may skip without tiktoken) |
| Unit tests | `python -m pytest tests -q` | No*** | No**** | All tests pass or expected skips |
| RAGAS | `python -m src.rag.step08_evaluate.run_practice_eval --framework ragas` | **Yes** | No | JSON `metrics` object |
| DeepEval | `python -m src.rag.step08_evaluate.run_practice_eval --framework deepeval` | **Yes** | No | `average_answer_relevancy` and per-sample scores |

\*Chunking validation uses **tiktoken** and may download `cl100k_base` on first run. If SSL fails on corporate networks, use hybrid validation and labs (offline section chunking) instead.

\*\*Lab 2 (parent–child) needs tiktoken.

\*\*\*Integration test `tests/test_step03_embedder.py` needs API if not ignored.

\*\*\*\*Pipeline API tests need DB when run.

### Phase 1 — Offline validation (≈10 minutes)

```powershell
cd c:\Learning\RAG\RAG_Process_445
.\.venv\Scripts\Activate.ps1

python -m src.ingestion.validate_loaders
python -m src.rag.step05_retrieve.validate_hybrid_search
python -m src.rag.step08_evaluate.run_practice_eval --mode offline --mock-retrieval --out data/processed/offline_eval_report.json
python -m src.rag.practice.run_labs
python -m pytest tests/test_bm25_hybrid.py tests/test_email_loader.py tests/test_practice_eval_offline.py -q
```

**Expected offline eval fields:**

```json
{
  "mode": "offline",
  "sample_count": 6,
  "keyword_hit_rate": 1.0,
  "retrieval": [ ... ]
}
```

### Phase 2 — Embedding validation (requires OpenAI)

```powershell
# Ensure OPENAI_API_KEY is set in .env
python -m src.rag.step03_embed.validate_embedding --list
python -m src.rag.step03_embed.validate_embedding
# Or subset:
python -m src.rag.step03_embed.validate_embedding 01 05 06
```

**Failure:** `ERROR: Set OPENAI_API_KEY in .env` → add key and retry.

### Phase 3 — Chunking comparison (requires tiktoken network or cache)

```powershell
python -m src.rag.step02_chunk.validate_chunking
```

### Phase 4 — LLM evaluation (optional deps)

```powershell
pip install -r requirements-eval.txt
python -m src.rag.step08_evaluate.run_practice_eval --framework ragas
python -m src.rag.step08_evaluate.run_practice_eval --framework deepeval
```

Save reports:

```powershell
python -m src.rag.step08_evaluate.run_practice_eval --mode offline --mock-retrieval --out data/processed/eval_report.json
```

---

## 6. Full application execution (API)

### 6.1 Start the API

```powershell
docker compose up -d
alembic upgrade head
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

| URL | Purpose |
|-----|---------|
| http://localhost:8000/ | Root info |
| http://localhost:8000/api/docs | Swagger UI |
| http://localhost:8000/api/v1/health | Health check |
| http://localhost:8000/metrics | Prometheus metrics |

**Health check:**

```powershell
Invoke-RestMethod http://localhost:8000/api/v1/health
```

Expected: `status: ok`

### 6.2 Ingest practice documents

**Local file path ingest** (use absolute or repo-relative path on the machine running the API):

```powershell
$body = @{
  source_type = "file"
  source_uri  = "c:\Learning\RAG\RAG_Process_445\data\examples\corpus\enterprise_hr_policy.md"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri "http://localhost:8000/api/v1/ingest/" `
  -ContentType "application/json" `
  -Body $body
```

**Email example:**

```powershell
$body = @{
  source_type = "email"
  source_uri  = "c:\Learning\RAG\RAG_Process_445\data\examples\emails\order_confirmation.eml"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri "http://localhost:8000/api/v1/ingest/" `
  -ContentType "application/json" `
  -Body $body
```

**File upload:**

```powershell
curl.exe -X POST "http://localhost:8000/api/v1/ingest/upload" `
  -F "file=@data/examples/corpus/acme_support_faq.md"
```

**Success:** Response includes `document_id`, `status: completed`.

**Side effects:**

- Rows in Postgres `documents` / `chunks`
- Vectors in Chroma under `CHROMA_PERSIST_DIR`
- BM25 lexical index updated at `data/processed/bm25_index.json` when `RETRIEVAL_MODE=hybrid`

### 6.3 Query

```powershell
$q = @{ question = "How many days of annual leave do full-time employees get?" } | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri "http://localhost:8000/api/v1/query/" `
  -ContentType "application/json" `
  -Body $q
```

**Success:**

- `answer` mentions **20 days** (if HR policy was indexed)
- `sources` is non-empty with `score` values
- `latency_ms` is present

**Empty or wrong answers:** Re-check indexing, `TOP_K`, `RETRIEVAL_MODE`, and that `OPENAI_API_KEY` is valid.

### 6.4 List documents

```powershell
Invoke-RestMethod http://localhost:8000/api/v1/documents/
```

---

## 7. Configuration change checklist

When you change settings, use this checklist:

| Change | Action required |
|--------|-----------------|
| `CHUNK_*`, `CHUNK_STRATEGY` | Re-ingest all documents |
| `EMBEDDING_MODEL` | Re-embed and re-index everything (new vector size) |
| `RETRIEVAL_MODE` | Re-ingest for BM25 sync; or run ingest again |
| `TOP_K`, `RERANK_*`, `USE_QUERY_TRANSFORM` | Restart API only |
| `DATABASE_URL` | Run `alembic upgrade head` on new DB |
| `CHROMA_PERSIST_DIR` | New empty index unless you copy old folder |

Restart uvicorn after `.env` changes (or reload if `--reload` is on).

---

## 8. Troubleshooting

### tiktoken / SSL: `CERTIFICATE_VERIFY_FAILED` when downloading `cl100k_base`

**Symptom:** `validate_chunking`, `TextChunker`, or Lab 2 fails on first run.

**Mitigations:**

1. Fix corporate SSL / proxy certificates for Python.
2. Use offline validators: `validate_hybrid_search`, `run_labs` (labs 1, 3–5).
3. Pre-cache tiktoken encoding on a machine with network access, then copy cache (advanced).

### pytest fails at collection (`deepeval` / `opik` plugins)

**Symptom:** Import errors from global packages during `pytest`.

**Fix:** Project `pytest.ini` includes `addopts = -p no:deepeval -p no:opik`. Run pytest from repo root.

### `test_offline_eval_runs_on_mock_data` retrieval count mismatch

**Symptom:** Expected 3 retrieval rows but dataset has 6 samples.

**Fix:** Test expects `len(report["retrieval"]) == report["sample_count"]` (current repo). Pull latest tests.

### Database connection errors

**Symptom:** API 500 on ingest/query.

**Checks:**

1. `docker compose ps` — Postgres healthy
2. `DATABASE_URL` matches Docker user/db/password
3. `alembic upgrade head` completed

### Chroma / stale index

**Symptom:** Query returns irrelevant chunks after corpus change.

**Fix:** Delete `data/chroma/` (and optionally `data/processed/bm25_index.json`), re-ingest all documents.

### URL ingest fails

**Symptom:** `UrlLoader` timeout or SSL.

**Checks:** `REQUEST_TIMEOUT_SECONDS`, network, URL reachable from server.

### Image ingest empty text

**Symptom:** OCR returns blank.

**Fix:** Install Tesseract; set `TESSERACT_CMD` to full executable path on Windows.

---

## 9. End-to-end validation script (manual checklist)

Print and tick through:

- [ ] `.venv` created, `pip install -r requirements.txt`
- [ ] `.env` created; `DATABASE_URL` matches Docker (if using API)
- [ ] Phase 1 offline commands all succeed
- [ ] `OPENAI_API_KEY` set; `validate_embedding` passes
- [ ] `docker compose up -d`; `alembic upgrade head`
- [ ] API health returns `ok`
- [ ] Ingest `enterprise_hr_policy.md` → `completed`
- [ ] Query annual leave → answer grounded in sources
- [ ] `run_practice_eval --mode offline --mock-retrieval` → JSON report saved
- [ ] (Optional) RAGAS or DeepEval run completes

---

## 10. Quick command reference

```powershell
# Setup
copy .env.example .env
pip install -r requirements.txt
docker compose up -d
alembic upgrade head

# Validate (offline)
python -m src.ingestion.validate_loaders
python -m src.rag.step05_retrieve.validate_hybrid_search
python -m src.rag.step08_evaluate.run_practice_eval --mode offline --mock-retrieval

# Validate (OpenAI)
python -m src.rag.step03_embed.validate_embedding

# Run API
uvicorn src.main:app --reload --port 8000

# Tests
python -m pytest tests/test_bm25_hybrid.py tests/test_practice_eval_offline.py -q
```

---

## 11. Source code map (configuration → behavior)

| Setting | Read in | Effect |
|---------|---------|--------|
| `chunk_strategy` | `src/rag/step07_pipeline/pipeline.py` | Chooses chunker via `get_chunker()` |
| `retrieval_mode` | `src/rag/step05_retrieve/retriever.py` | Vector-only vs hybrid RRF |
| `use_query_transform` | `retriever.py` | Acronym expansion before embed |
| `rerank_mode` | `reranker.py` | Post-retrieval reorder |
| `embedding_model` / `llm_model` | `embedder.py`, `generator.py` | OpenAI model IDs |
| `chroma_persist_dir` | `vector_store.py` | Local vector persistence |

For architecture context, see [08-enterprise-architecture.md](08-enterprise-architecture.md).
