import time

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.api.schemas import QueryRequest, QueryResponse, SourceChunk
from src.metrics.prometheus import QUERY_COUNTER, QUERY_LATENCY
from src.services.rag_service import RAGService

router = APIRouter(prefix="/query", tags=["Query"])


@router.post("/", response_model=QueryResponse)
def ask_question(payload: QueryRequest, db: Session = Depends(get_db)):
    start = time.perf_counter()

    service = RAGService(db)
    result = service.ask(payload.question)

    latency_ms = (time.perf_counter() - start) * 1000

    QUERY_COUNTER.inc()
    QUERY_LATENCY.observe(latency_ms / 1000)

    return QueryResponse(
        answer=result.answer,
        sources=[
            SourceChunk(
                chunk_id=source.chunk_id,
                content=source.content,
                score=source.score,
            )
            for source in result.sources
        ],
        latency_ms=latency_ms,
    )