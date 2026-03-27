"""
Aplicação FastAPI — Diamond Price Predictor.

Endpoints:
    GET  /health   → Verificação de saúde
    GET  /info     → Metadados do modelo
    POST /predict  → Predição de preço do diamante
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app import model as model_module
from app.config import APP_DESCRIPTION, APP_TITLE, APP_VERSION
from app.schemas import (
    HealthResponse,
    ModelInfoResponse,
    DiamondFeatures,
    PriceResponse,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carrega o modelo antes de aceitar requisições; libera ao encerrar."""
    logger.info("Iniciando API — carregando modelo Diamond Price...")
    model_module.load_model()
    yield
    logger.info("Encerrando API.")


app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse, tags=["Monitoramento"])
def health_check():
    """Verifica se a API está operacional e se o modelo foi carregado."""
    return HealthResponse(
        status="ok",
        model_loaded=model_module.is_model_loaded(),
        version=APP_VERSION,
    )


@app.get(
    "/info",
    response_model=ModelInfoResponse,
    tags=["Monitoramento"],
)
def model_info():
    """Retorna metadados do modelo carregado (algoritmo, features, métricas)."""
    if not model_module.is_model_loaded():
        raise HTTPException(status_code=503, detail="Modelo não disponível.")
    return ModelInfoResponse(
        version=APP_VERSION,
        algorithm=model_module.get_algorithm(),
        features=model_module.get_features(),
        target="price (USD)",
        metrics=model_module.get_metrics(),
    )


@app.post("/predict", response_model=PriceResponse, tags=["Predição"])
def predict(features: DiamondFeatures):
    """
    Estima o preço de um diamante com base nas suas características físicas.

    Valida os limites físicos do dataset (carat, depth, table, x, y, z)
    e os valores categóricos válidos (cut, color, clarity) antes de inferir.
    """
    try:
        return model_module.predict(features)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
