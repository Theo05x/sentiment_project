# Model loader (placeholder)

from pathlib import Path
import joblib
import logging
from app.config import settings
from typing import Tuple, Optional
from app.core.preprocess import Preprocessor

logger = logging.getLogger(__name__)


class SentimentModel:
    """Carga el pipeline de forma lazy (solo al predecir).

    Si no existe o falla la carga, usa heurísticos simples.
    """
    def __init__(self, model_path: Optional[Path] = None):
        self.model_path = Path(model_path) if model_path else settings.MODEL_PATH
        self.pipe = None
        self.pre = Preprocessor()

    def _ensure_loaded(self):
        if self.pipe is not None:
            return
        if self.model_path.exists():
            try:
                self.pipe = joblib.load(self.model_path)
                logger.info("Modelo cargado desde %s", self.model_path)
            except Exception:
                logger.exception("Fallo cargando el modelo desde %s", self.model_path)
                self.pipe = None
        else:
            logger.info("Archivo de modelo no encontrado en %s, usando heurísticos", self.model_path)

    def predict(self, text: str) -> Tuple[str, Optional[float]]:
        txt = self.pre.clean_text(text)
        # intentar cargar modelo si está disponible
        self._ensure_loaded()

        if self.pipe is None:
            t = txt.lower()
            if any(w in t for w in ["bad", "terrible", "hate", "worst", "delay", "angry", "problem"]):
                return "negative", 0.85
            if any(w in t for w in ["good", "great", "love", "awesome", "thanks", "perfect", "happy"]):
                return "positive", 0.85
            return "neutral", 0.5

        try:
            preds = self.pipe.predict([txt])
            prob = None
            if hasattr(self.pipe, "predict_proba"):
                proba = self.pipe.predict_proba([txt])[0]
                idx = list(self.pipe.classes_).index(preds[0])
                prob = float(proba[idx])
            return str(preds[0]), prob
        except Exception:
            logger.exception("Error during prediction")
            return "neutral", None
