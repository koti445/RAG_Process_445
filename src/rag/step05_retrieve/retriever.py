import uuid

from src.core.config import get_settings
from src.domain.models import RetrievalResult
from src.rag.step03_embed.embedder import Embedder
from src.rag.step04_store.vector_store import VectorStore


class Retriever:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.embedder = Embedder()
        self.vector_store = VectorStore()

    def retrieve(self, question: str, top_k: int | None = None) -> list[RetrievalResult]:
        k = top_k or self.settings.top_k
        query_embedding = self.embedder.embed_query(question)
        results = self.vector_store.search(query_embedding, k)

        retrieved: list[RetrievalResult] = []
        if not results.get("ids") or not results["ids"][0]:
            return retrieved

        for i, chunk_id in enumerate(results["ids"][0]):
            content = results["documents"][0][i]
            distance = results["distances"][0][i]
            score = 1 - distance
            metadata = results["metadatas"][0][i] if results.get("metadatas") else {}

            retrieved.append(
                RetrievalResult(
                    chunk_id=uuid.UUID(chunk_id),
                    content=content,
                    score=score,
                    metadata=metadata or {},
                )
            )

        return retrieved