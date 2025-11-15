# Pydantic schemas (placeholder)

from pydantic import BaseModel
from typing import Optional, List, Dict

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    label: str
    score: Optional[float]

class IngestResponse(BaseModel):
    rows_loaded: int

class MetricsSummary(BaseModel):
    total_tweets: int
    by_sentiment: Dict[str,int]
    top_airlines: List[Dict[str,int]]
