import time
import uuid

from sqlalchemy.orm import Session

from src.core.config import get_settings
from src.db.models import ChunkORM, DocumentORM, QueryLogORM
from src.domain.models import RAGResponse
from src.metrics.prometheus import CHUNK_COUNT
from src.rag.step02_chunk.chunker import TextChunker
from src.rag.step03_embed.embedder import Embedder
from src.rag.step04_store.vector_store import VectorStore
from src.rag.step05_retrieve.retriever import Retriever
from src.rag.step06_generate.generator import Generator


class RAGPipeline:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.settings = get_settings()
        self.chunker = TextChunker()
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        self.retriever = Retriever()
        self.generator = Generator()

    def index_document(self, document: DocumentORM, content: str) -> int:
        chunks = self.chunker.chunk(content, metadata={"document_id": str(document.id)})
        if not chunks:
            document.status = "failed"
            self.db.commit()
            return 0

        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedder.embed_texts(texts)

        chunk_rows: list[ChunkORM] = []
        vector_ids: list[str] = []
        metadatas: list[dict] = []

        for chunk, embedding in zip(chunks, embeddings):
            chunk_id = uuid.uuid4()
            vector_id = str(chunk_id)

            row = ChunkORM(
                id=chunk_id,
                document_id=document.id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                token_count=chunk.token_count,
                vector_id=vector_id,
                chunk_metadata=chunk.metadata,
            )
            chunk_rows.append(row)
            vector_ids.append(vector_id)
            metadatas.append({"document_id": str(document.id)})

        self.db.add_all(chunk_rows)
        self.vector_store.add(
            ids=vector_ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )

        document.status = "indexed"
        self.db.commit()

        CHUNK_COUNT.inc(len(chunk_rows))
        return len(chunk_rows)

    def query(self, question: str) -> RAGResponse:
        start = time.perf_counter()

        sources = self.retriever.retrieve(question)
        context_texts = [source.content for source in sources]
        answer = self.generator.generate(question, context_texts)

        latency_ms = (time.perf_counter() - start) * 1000

        log = QueryLogORM(
            question=question,
            answer=answer,
            sources=[
                {"chunk_id": str(source.chunk_id), "score": source.score}
                for source in sources
            ],
            latency_ms=latency_ms,
        )
        self.db.add(log)
        self.db.commit()

        return RAGResponse(answer=answer, sources=sources)