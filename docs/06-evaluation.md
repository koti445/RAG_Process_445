# Step 8 — Evaluation

You need scores at **three layers**:

1. **Retrieval** — did we fetch the right chunks? (precision, recall, MRR, nDCG)
2. **Generation** — is the answer grounded and on-topic?
3. **End-to-end** — would a user trust the reply?

## Offline practice (no API cost)

Mock data: `data/examples/eval/eval_dataset.json`

```powershell
python -m src.rag.step08_evaluate.run_practice_eval --mode offline --mock-retrieval
```

Output includes:

- `keyword_hit_rate` — simple answer check using `expected_keywords`
- `retrieval` — precision@3, recall@3, MRR, nDCG@3 per question

Code:

- Metrics: `src/rag/step08_evaluate/retrieval_metrics.py`
- Keyword check: `src/rag/step08_evaluate/evaluator.py`

## RAGAS (optional)

Install: `pip install -r requirements-eval.txt`

```powershell
python -m src.rag.step08_evaluate.run_practice_eval --framework ragas
```

Typical metrics: faithfulness, answer relevancy, context precision.

Runner: `src/rag/step08_evaluate/ragas_runner.py`

## DeepEval (optional)

```powershell
python -m src.rag.step08_evaluate.run_practice_eval --framework deepeval
```

Uses `AnswerRelevancyMetric` per sample.

Runner: `src/rag/step08_evaluate/deepeval_runner.py`

> Both frameworks call an LLM — set `OPENAI_API_KEY` in `.env`.

## Wiring real pipeline answers into eval

1. Index `data/examples/corpus/acme_support_faq.md` through the API or pipeline.
2. For each row in `eval_dataset.json`, call `RAGPipeline.query(question)`.
3. Pass `answer` and retrieved `contexts` into RAGAS/DeepEval instead of mock answers.

## Criticality

| Severity | Without evaluation… |
|----------|---------------------|
| High | You ship a demo that fails on easy FAQ questions. |
| Medium | You cannot compare chunk sizes, rerankers, or models objectively. |

Next: [07-step-criticality.md](07-step-criticality.md).
