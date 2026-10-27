# RAG for beginners (simple story)

Imagine you have a **big box of papers** (your company documents). A friend asks: *"How long is the laptop warranty?"*

You do not read every paper from start to finish. You:

1. **Collect** the right papers (ingestion).
2. **Cut** long papers into small sticky notes (chunking).
3. **Label** each note with a secret number code that captures meaning (embedding).
4. **File** notes in a magic cabinet that finds similar codes (vector database / Chroma).
5. **Search** the cabinet with the question’s code (retrieval).
6. **Reorder** the best notes to the top (reranking — optional but helpful).
7. **Answer** using only those notes (generation).
8. **Check** if the answer was fair and correct (evaluation).

That is **RAG**: **Retrieval-Augmented Generation**.

## Map to this project

| Story step | Folder in code |
|------------|----------------|
| Collect papers | `src/ingestion/loaders/` |
| Cut into notes | `src/rag/step02_chunk/` |
| Secret number codes | `src/rag/step03_embed/` |
| Magic filing cabinet | `src/rag/step04_store/` (Chroma) + Postgres for records |
| Find similar notes | `src/rag/step05_retrieve/` |
| Put best notes first | `src/rag/step05_retrieve/reranker.py` |
| Write the answer | `src/rag/step06_generate/` |
| Full journey | `src/rag/step07_pipeline/pipeline.py` |
| Did we do well? | `src/rag/step08_evaluate/` |

## Practice data (no setup drama)

We ship a tiny fake company **ACME Gadgets** in `data/examples/`:

- `corpus/acme_support_faq.md` — documents to index
- `eval/eval_dataset.json` — questions + expected answers for metrics
- `emails/order_confirmation.eml` — sample email ingestion

## What you need on your computer

- **Python 3.11+**
- **Docker** (for Postgres + Chroma via `docker-compose.yml`) when running the API
- **OpenAI API key** for real embeddings and chat (put in `.env`)
- **Tesseract** (optional) for image OCR

## First win (5 minutes, no API)

```powershell
python -m src.ingestion.validate_loaders
python -m src.rag.step02_chunk.validate_chunking
python -m src.rag.step08_evaluate.run_practice_eval --mode offline --mock-retrieval
```

You should see loader previews, chunk counts per strategy, and a JSON report with keyword hit rate and retrieval scores.

When you are ready for **company-style** examples (HR, IT SLA, VPN), open:

- `data/examples/corpus/enterprise_hr_policy.md`
- `data/examples/corpus/enterprise_it_runbook.md`
- [11-hands-on-labs.md](11-hands-on-labs.md)

Full curriculum: [00-learning-path.md](00-learning-path.md).

Next: read [02-ingestion.md](02-ingestion.md).
