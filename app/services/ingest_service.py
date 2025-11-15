# ingest service (placeholder)

# app/services/ingest_service.py
from fastapi import UploadFile
import pandas as pd
from pathlib import Path
from app.config import settings
import io

class IngestService:
    def __init__(self, storage_path: Path | None = None):
        self.storage = Path(storage_path) if storage_path else settings.DATA_PATH

    async def ingest_csv(self, file: UploadFile):
        contents = await file.read()
        s = contents.decode('utf-8', errors='replace')
        # leer con separador ; y saltar líneas problemáticas
        df = pd.read_csv(io.StringIO(s), sep=";", on_bad_lines='skip', engine='python')

        # normalizar columnas esperadas y parsear fechas
        if 'tweet_created' in df.columns:
            try:
                df['tweet_created'] = pd.to_datetime(df['tweet_created'], dayfirst=True, errors='coerce')
            except Exception:
                df['tweet_created'] = pd.to_datetime(df['tweet_created'], errors='coerce')

        # asegurar columnas mínimas
        expected = ['text', 'airline_sentiment', 'sentiment', 'name', 'retweet_count', 'tweet_location', 'tweet_created']
        for c in expected:
            if c not in df.columns:
                df[c] = None

        self.storage.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.storage, index=False, sep=';')
        return df
