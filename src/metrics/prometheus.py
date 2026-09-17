from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

INGESTION_COUNTER = Counter(
    "rag_ingestion_total",
    "Total ingestion jobs",
    ["status"],
)

QUERY_COUNTER = Counter(
    "rag_query_total",
    "Total RAG queries",
)

QUERY_LATENCY = Histogram(
    "rag_query_latency_seconds",
    "RAG query latency in seconds",
)

CHUNK_COUNT = Counter(
    "rag_chunks_indexed_total",
    "Total chunks indexed",
)


def metrics_response() -> tuple[bytes, str]:
    return generate_latest(), CONTENT_TYPE_LATEST