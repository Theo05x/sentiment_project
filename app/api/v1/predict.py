# Prediction endpoints (placeholder)

from fastapi import APIRouter, HTTPException
from app.schemas.pydantic_schemas import PredictRequest, PredictResponse
from app.services.sentiment_service import SentimentService

router = APIRouter()
service = SentimentService()

@router.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        label, score = service.predict(req.text)
        return PredictResponse(label=label, score=score)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
