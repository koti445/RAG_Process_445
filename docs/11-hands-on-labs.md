# Hands-on labs

Run all labs:

```powershell
python -m src.rag.practice.run_labs
```

Or one at a time: `python -m src.rag.practice.run_labs --lab 3`

---

## Lab 1 — Chunk strategy comparison

**Learn:** chunk size changes recall and noise.

**Do:** Run lab 1; note which strategy gives the fewest chunks for `enterprise_it_runbook.md`.

**Checkpoint:** You can explain when to pick `sentence` vs `token`.

---

## Lab 2 — Parent–child chunking

**Learn:** small chunks for search, big chunks for reading.

**Do:** Run lab 2; inspect `parent_id` on child metadata.

**Checkpoint:** Describe how you would fetch parent text after a child hit.

---

## Lab 3 — BM25 + RRF

**Learn:** hybrid beats pure vector on acronym-heavy IT questions.

**Do:** Run lab 3 and `python -m src.rag.step05_retrieve.validate_hybrid_search`.

**Checkpoint:** Explain RRF in one sentence (merge ranked lists without tuning weights).

---

## Lab 4 — Query transform

**Learn:** expand VPN/SLA/PII before embedding.

**Do:** Run lab 4; try your own question with acronyms.

**Checkpoint:** Compare `original` vs `rewritten` strings.

---

## Lab 5 — Evaluation report

**Learn:** keyword hits + retrieval metrics on mock enterprise Q&A.

**Do:** Run lab 5; open `data/examples/eval/eval_dataset.json` and add one new row for HR.

**Checkpoint:** Re-run lab 5 and see `sample_count` increase.

---

## Lab 6 — End-to-end (with API key)

**Learn:** real embeddings + generation.

**Do:**

1. Set `OPENAI_API_KEY` in `.env`.
2. Start Postgres + app; index `enterprise_hr_policy.md` via ingestion API.
3. Ask: *"How many sick days per year?"*
4. Run RAGAS: `python -m src.rag.step08_evaluate.run_practice_eval --framework ragas`

**Checkpoint:** Answer cites sick leave policy; eval metrics print without errors.

---

## Instructor rubric (self-check)

| Skill | Evidence |
|-------|----------|
| Ingestion | Loader validation passes on email + markdown |
| Chunking | Strategy comparison table written in your notes |
| Retrieval | Hybrid demo finds SLA / VPN snippets |
| Eval | Offline report JSON saved to `data/processed/lab5_report.json` |

```powershell
python -m src.rag.step08_evaluate.run_practice_eval --mode offline --mock-retrieval --out data/processed/lab5_report.json
```
