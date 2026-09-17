from sqlalchemy.orm import Session

from src.domain.models import RAGResponse
from src.rag.step07_pipeline.pipeline import RAGPipeline


class RAGService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.pipeline = RAGPipeline(db)

    def ask(self, question: str) -> RAGResponse:
        return self.pipeline.query(question)