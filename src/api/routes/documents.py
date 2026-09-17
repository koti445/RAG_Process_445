from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.api.schemas import DocumentResponse
from src.db.models import DocumentORM

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(DocumentORM).order_by(DocumentORM.created_at.desc()).all()
    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: UUID, db: Session = Depends(get_db)):
    document = db.get(DocumentORM, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document