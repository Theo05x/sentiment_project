# Metrics endpoints (placeholder)

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.metrics_service import MetricsService

router = APIRouter()
service = MetricsService()


@router.get("/summary")
def summary():
    return service.sentiment_summary()


@router.get("/time_series")
def time_series(freq: Optional[str] = Query('D', description="Aggregation frequency: D,W,M")):
    return service.sentiment_time_series(freq)


@router.get("/keywords")
def keywords(sentiment: Optional[str] = Query(None), top: int = Query(50)):
    return {"keywords": service.top_keywords(sentiment, top)}


@router.get("/topics")
def topics(sentiment: str = Query('negative')):
    return {"topics": service.topic_breakdown(sentiment)}


@router.get("/influencers")
def influencers(sentiment: Optional[str] = Query(None), limit: int = Query(20), sort_by: Optional[str] = Query('count')):
    return {"influencers": service.top_influencers(sentiment, limit, sort_by)}


@router.get("/geo")
def geo(top: int = Query(100)):
    return {"geo": service.geo_distribution(top)}


@router.post("/recompute")
def recompute():
    service.clear_cache()
    return {"status": "ok"}
