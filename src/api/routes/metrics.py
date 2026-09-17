from fastapi import APIRouter, Response

from src.metrics.prometheus import metrics_response

router = APIRouter(tags=["Metrics"])


@router.get("/metrics")
def prometheus_metrics():
    content, content_type = metrics_response()
    return Response(content=content, media_type=content_type)