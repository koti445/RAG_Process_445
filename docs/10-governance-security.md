# Governance, security, and responsible RAG

## Data handling

| Rule | Practice |
|------|----------|
| Least privilege | Only index sources the app may read |
| Classification | Store `classification` on chunks; filter queries for user role |
| PII | Redact before index or block at ingestion (HR/health data) |
| Retention | Delete vectors when document deleted (`VectorStore.delete`) |

## Prompt and answer safety

The generator already:

- Uses **context-only** answers.
- Says *"I don't have enough information"* when context is empty.

Enterprise additions (patterns to implement):

- **Citation required** — answer must reference chunk ids.
- **Blocked topics** — legal/medical disclaimers.
- **Output filters** — regex or moderation API on responses.

## Audit trail

| Event | Where |
|-------|-------|
| Questions asked | `query_logs` in Postgres |
| Sources used | `sources` JSON on each log row |
| Latency | `latency_ms` + Prometheus histogram |

## Evaluation as governance

Run before each release:

```powershell
python -m src.rag.step08_evaluate.run_practice_eval --mode offline --mock-retrieval
```

Add domain-specific rows to `data/examples/eval/eval_dataset.json` for HR, IT, and support.

Optional LLM judges:

```powershell
pip install -r requirements-eval.txt
python -m src.rag.step08_evaluate.run_practice_eval --framework ragas
```

## Third-party models

- Send only necessary text to embedding/chat APIs.
- Use enterprise agreements (Azure OpenAI, private endpoints) in production.
- Never commit `.env` or customer dumps to git.

Next: [11-hands-on-labs.md](11-hands-on-labs.md).
