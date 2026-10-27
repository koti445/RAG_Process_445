# Step 2 — Chunking (cut text into pieces)

**Goal:** Pieces must be **small enough** for the embedding model and **big enough** to keep meaning.

## Strategies (`src/rag/step02_chunk/chunk_strategies.py`)

| Strategy | When to use |
|----------|-------------|
| `token` | Default; fixed token windows with overlap (`CHUNK_SIZE`, `CHUNK_OVERLAP`) |
| `sentence` | FAQ / policies where sentences should stay whole |
| `paragraph` | Docs with clear blank-line sections |
| `recursive` | Mixed layouts; splits on `\n\n`, then `\n`, then words |

Set in `.env`:

```env
CHUNK_STRATEGY=token
```

## Compare strategies on practice corpus

```powershell
python -m src.rag.step02_chunk.validate_chunking
```

## Code example

```python
from src.rag.step02_chunk.chunk_strategies import ChunkStrategy, get_chunker

text = open("data/examples/corpus/acme_support_faq.md", encoding="utf-8").read()
chunks = get_chunker(ChunkStrategy.SENTENCE).chunk(text)
print(len(chunks), chunks[0].content[:80])
```

## Criticality

| Severity | If chunking is wrong… |
|----------|------------------------|
| High | Answers miss facts split across chunks, or noise floods retrieval. |
| Medium | Too much overlap → duplicate hits; too little → lost context. |

Next: [04-embedding-and-index.md](04-embedding-and-index.md).
