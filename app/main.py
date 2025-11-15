# FastAPI entrypoint (placeholder)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import api_router
from app.config import settings
import logging


def create_app():
    # logging básico
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    app = FastAPI(title="Sentiment Analysis API", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)

    @app.on_event("startup")
    async def _startup_event():
        logger = logging.getLogger("uvicorn")
        logger.info("App startup. PROJECT_ROOT=%s, DATA_PATH=%s, MODEL_PATH=%s", settings.PROJECT_ROOT, settings.DATA_PATH, settings.MODEL_PATH)

    return app


app = create_app()


@app.get("/health")
def health():
    return {"status": "ok"}
