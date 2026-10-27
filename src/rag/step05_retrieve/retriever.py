import uuid

from src.core.config import get_settings
from src.domain.models import RetrievalResult
from src.rag.step03_embed.embedder import Embedder
from src.rag.step04_store.vector_store import VectorStore
from src.rag.step05_retrieve.hybrid_search import fuse_vector_and_lexical
from src.rag.step05_retrieve.lexical_index import get_lexical_index
from src.rag.step05_retrieve.query_transform import transform_query
from src.rag.step05_retrieve.reranker import get_reranker


class Retriever:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        self.reranker = get_reranker(
            self.settings.rerank_mode,
            cross_encoder_model=self.settings.rerank_cross_encoder_model,
        )

    def retrieve(
        self,
        question: str,
        top_k: int | None = None,
        metadata_filter: dict | None = None,
    ) -> list[RetrievalResult]:
        k = top_k or self.settings.top_k
        search_text = question
        if self.settings.use_query_transform:
            search_text = transform_query(question).rewritten

        query_embedding = self.embedder.embed_query(search_text)
        fetch_k = k * 3 if self.settings.retrieval_mode == "hybrid" else k
        results = self.vector_store.search(query_embedding, fetch_k, where=metadata_filter)

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

        if self.settings.retrieval_mode == "hybrid":
            retrieved = fuse_vector_and_lexical(
                question=search_text,
                vector_results=retrieved,
                lexical_index=get_lexical_index(),
                top_k=k,
            )

        return self.reranker.rerank(question, retrieved)