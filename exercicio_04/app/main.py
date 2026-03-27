import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.config import APP_TITLE, APP_DESCRIPTION, APP_VERSION
from app import model as model_module
from app.schemas import (
    HeartPatientFeatures, HeartRiskResponse, HealthResponse, ModelInfoResponse
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        model_module.load_model()
    except Exception as e:
        logger.error(f"Erro no startup: {e}")
    yield
    # Shutdown
    logger.info("Encerrando API.")

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan
)

@app.get("/health", response_model=HealthResponse, tags=["Monitoramento"])
def health():
    return HealthResponse(
        status="ok",
        model_loaded=model_module.is_model_loaded()
    )

@app.get("/info", response_model=ModelInfoResponse, tags=["Monitoramento"])
def info():
    data = model_module.get_info()
    if not data:
        raise HTTPException(status_code=503, detail="Modelo não carregado.")
    return ModelInfoResponse(**data)

@app.post("/predict", response_model=HeartRiskResponse, tags=["Predição"])
def predict(features: HeartPatientFeatures):
    try:
        return model_module.predict(features)
    except Exception as e:
        logger.error(f"Erro na predição: {e}")
        raise HTTPException(status_code=500, detail="Erro interno na predição.")
