from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.api.schemas import IngestRequest, IngestResponse
from src.core.config import get_settings
from src.core.enums import SourceType
from src.services.ingestion_service import IngestionService

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("/", response_model=IngestResponse)
def ingest_from_uri(payload: IngestRequest, db: Session = Depends(get_db)):
    service = IngestionService(db)
    job = service.create_job(payload.source_type, payload.source_uri)

    try:
        document = service.run_job(job.id)
        return IngestResponse(
            job_id=job.id,
            document_id=document.id,
            status="completed",
            message="Document indexed successfully",
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/upload", response_model=IngestResponse)
async def ingest_upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    settings = get_settings()
    content = await file.read()

    if len(content) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail="File too large")

    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    save_path = settings.data_raw_dir / file.filename
    save_path.write_bytes(content)

    suffix = Path(file.filename).suffix.lower()
    source_type = SourceType.FILE

    if suffix == ".zip":
        source_type = SourceType.ZIP
    elif suffix in {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}:
        source_type = SourceType.IMAGE
    elif suffix in {".mp4", ".avi", ".mov", ".mkv"}:
        source_type = SourceType.VIDEO

    service = IngestionService(db)
    job = service.create_job(source_type, str(save_path))

    try:
        document = service.run_job(job.id)
        return IngestResponse(
            job_id=job.id,
            document_id=document.id,
            status="completed",
            message=f"Indexed {file.filename}",
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc