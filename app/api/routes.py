# Router aggregator (placeholder)

from fastapi import APIRouter
from app.api.v1 import predict, ingest, metrics

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(predict.router, prefix="/predict", tags=["predict"])
api_router.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
