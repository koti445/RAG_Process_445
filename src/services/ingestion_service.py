import uuid
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from src.core.enums import IngestionStatus, SourceType
from src.db.models import DocumentORM, IngestionJobORM
from src.ingestion.registry import get_loader
from src.metrics.prometheus import INGESTION_COUNTER
from src.rag.step07_pipeline.pipeline import RAGPipeline


class IngestionService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_job(self, source_type: SourceType, source_uri: str) -> IngestionJobORM:
        job = IngestionJobORM(
            source_type=source_type.value,
            source_uri=source_uri,
            status=IngestionStatus.PENDING.value,
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def run_job(self, job_id: uuid.UUID) -> DocumentORM:
        job = self.db.get(IngestionJobORM, job_id)
        if job is None:
            raise ValueError(f"Ingestion job not found: {job_id}")

        job.status = IngestionStatus.PROCESSING.value
        self.db.commit()

        try:
            loader = get_loader(SourceType(job.source_type))
            loaded_docs = loader.load(job.source_uri)

            if not loaded_docs:
                raise ValueError("Loader returned no documents")

            combined_text = "\n\n".join(doc.content for doc in loaded_docs if doc.content.strip())
            if not combined_text.strip():
                raise ValueError("No extractable text found in source")

            title = self._build_title(job.source_type, job.source_uri)

            document = DocumentORM(
                title=title,
                source_type=job.source_type,
                source_uri=job.source_uri,
                status="uploaded",
                doc_metadata=loaded_docs[0].metadata,
            )
            self.db.add(document)
            self.db.flush()

            pipeline = RAGPipeline(self.db)
            chunk_count = pipeline.index_document(document, combined_text)

            job.status = IngestionStatus.COMPLETED.value
            job.document_id = document.id
            job.completed_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(document)

            INGESTION_COUNTER.labels(status="completed").inc()
            return document

        except Exception as exc:
            job.status = IngestionStatus.FAILED.value
            job.error_message = str(exc)
            job.completed_at = datetime.utcnow()
            self.db.commit()
            INGESTION_COUNTER.labels(status="failed").inc()
            raise

    @staticmethod
    def _build_title(source_type: str, source_uri: str) -> str:
        if source_type in {"file", "zip", "image", "video"}:
            return Path(source_uri).name
        return source_uri[:200]