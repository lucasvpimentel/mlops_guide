import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.config import APP_TITLE, APP_DESCRIPTION, APP_VERSION
from app import model as model_module
from app.schemas import (
    BuildingFeatures,
    HeatingLoadResponse,
    HealthResponse,
    ModelInfoResponse
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Carregar o modelo do arquivo .joblib
    logger.info("Iniciando API... carregando artefatos de ML.")
    try:
        model_module.load_model()
    except Exception as e:
        logger.critical(f"Falha catastrófica ao carregar o modelo: {e}")
        # Em produção, isso impediria o container de subir.
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
def health_check():
    """
    Verifica se a API está online e se o modelo foi carregado
    corretamente.
    """
    return HealthResponse(
        status="ok",
        model_loaded=model_module.is_model_loaded(),
        version=APP_VERSION
    )


@app.get("/info", response_model=ModelInfoResponse, tags=["Monitoramento"])
def model_info():
    """Retorna metadados do modelo treinado (métricas e features)."""
    if not model_module.is_model_loaded():
        raise HTTPException(status_code=503, detail="Modelo não disponível.")

    return ModelInfoResponse(
        version=APP_VERSION,
        features=model_module.get_model_features(),
        metrics=model_module.get_model_metrics()
    )


@app.post("/predict", response_model=HeatingLoadResponse, tags=["Predição"])
def predict(features: BuildingFeatures):
    """
    Realiza a predição da carga de aquecimento (Heating Load).
    Valida as restrições físicas dos campos conforme o dataset UCI.
    """
    try:
        return model_module.predict(features)
    except Exception as e:
        logger.error(f"Erro na predição: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal prediction error."
        )
