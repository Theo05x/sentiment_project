# app/config.py
from pathlib import Path
import os


# Simple settings object that does not require pydantic; reads from env with sensible defaults.
class Settings:
    def __init__(self):
        self.PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
        # Default data path inside the repo (app/data)
        default_data = self.PROJECT_ROOT / "app" / "data" / "df_twitter_prueba4.csv"
        self.DATA_PATH: Path = Path(os.getenv("DATA_PATH", default_data))
        # model and vectorizer paths inside the app core
        self.MODEL_PATH: Path = Path(os.getenv("MODEL_PATH", str(self.PROJECT_ROOT / "app" / "core" / "model.joblib")))
        self.VECTORIZER_PATH: Path = Path(os.getenv("VECTORIZER_PATH", str(self.PROJECT_ROOT / "app" / "core" / "vectorizer.joblib")))


settings = Settings()

