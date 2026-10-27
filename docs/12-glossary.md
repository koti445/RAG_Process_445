# Glossary (plain language)

| Term | Meaning |
|------|---------|
| **RAG** | Retrieve relevant text, then let the AI answer using that text. |
| **Chunk** | A small piece of a document after splitting. |
| **Embedding** | A list of numbers representing meaning; similar text → similar numbers. |
| **Vector database** | Stores embeddings and finds nearest neighbors quickly. |
| **Top-k** | How many chunks to fetch (e.g. 5). |
| **BM25** | Keyword search scoring (good for exact words). |
| **Hybrid search** | Vector + keyword, often fused with RRF. |
| **RRF** | Reciprocal Rank Fusion — merges ranked lists without mixing incomparable scores. |
| **Reranking** | Second model reorders top candidates for better precision. |
| **Hallucination** | AI invents facts not in the documents. |
| **Grounding** | Forcing answers to use retrieved context only. |
| **Faithfulness** | Eval metric: is the answer supported by context? |
| **Metadata filter** | Search only chunks tagged e.g. `department=it`. |
| **Parent–child chunks** | Small pieces for search; large parent for LLM context. |
| **SLA** | Service level agreement — promised response/resolution times. |
| **PII** | Personally identifiable information about people. |
| **RBAC** | Role-based access control — who may see which data. |
