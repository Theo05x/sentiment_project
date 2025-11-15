# Sentiment service (placeholder)

from app.core.model import SentimentModel

class SentimentService:
    def __init__(self, model_path=None):
        self.model = SentimentModel(model_path)

    def predict(self, text: str):
        label, score = self.model.predict(text)
        return label, score
