# Ingest endpoints (placeholder)

from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.ingest_service import IngestService
from app.schemas.pydantic_schemas import IngestResponse

router = APIRouter()
service = IngestService()

@router.post("/ingest_csv", response_model=IngestResponse)
async def ingest_csv(file: UploadFile = File(...)):
    try:
        df = await service.ingest_csv(file)
        return IngestResponse(rows_loaded=len(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
