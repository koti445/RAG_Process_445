# Step 1 — Ingestion (get text from many sources)

**Goal:** Turn files and links into plain `LoadedDocument` text the rest of the pipeline can use.

## Supported types in this repo

| Type | Extension / source | Loader | Notes |
|------|-------------------|--------|-------|
| Text | `.txt`, `.md` | `FileLoader` | UTF-8 text |
| PDF | `.pdf` | `FileLoader` | One `LoadedDocument` per page |
| Word | `.docx` | `FileLoader` | Needs `python-docx` |
| Email | `.eml` | `EmailLoader` | Headers + plain body |
| Web page | `http(s) URL` | `UrlLoader` | Strips nav/scripts; needs network |
| Image | `.png`, `.jpg`, … | `ImageLoader` | OCR via Tesseract |
| Zip | `.zip` | `ZipLoader` | Extracts supported inner files |
| Video | video files | `VideoLoader` | Metadata / transcript hooks |

Registry: `src/ingestion/registry.py` maps `SourceType` → loader.

## Validate without the API

```powershell
python -m src.ingestion.validate_loaders
```

## Try email + markdown yourself

```python
from src.ingestion.loaders.file_loader import FileLoader
from src.ingestion.loaders.email_loader import EmailLoader

faq = FileLoader().load("data/examples/corpus/acme_support_faq.md")
email = EmailLoader().load("data/examples/emails/order_confirmation.eml")
print(faq[0].content[:200])
print(email[0].metadata["subject"])
```

## Common mistakes

- **Empty PDF text** — scanned PDFs need OCR (image pipeline), not only `pypdf`.
- **Wrong encoding** — non-UTF8 `.txt` may need conversion before load.
- **Huge files** — respect `MAX_UPLOAD_MB` in settings.

## Criticality

| Severity | If ingestion fails… |
|----------|---------------------|
| High | Nothing downstream has text to chunk; RAG answers become guesses. |

Next: [03-chunking.md](03-chunking.md).
