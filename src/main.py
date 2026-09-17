from fastapi import FastAPI

from src.api.routes import documents, health, ingestion, metrics, query
from src.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(documents.router, prefix=settings.api_prefix)
app.include_router(ingestion.router, prefix=settings.api_prefix)
app.include_router(query.router, prefix=settings.api_prefix)
app.include_router(metrics.router)


@app.get("/")
def root():
    return {
        "message": "RAG API running",
        "swagger": "/api/docs",
        "metrics": "/metrics",
    }