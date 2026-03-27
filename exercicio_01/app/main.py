import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app import model as model_module
from app.config import APP_DESCRIPTION, APP_TITLE, APP_VERSION
from app.schemas import (
    HealthResponse,
    ModelInfoResponse,
    PenguinFeatures,
    PredictionResponse,
)

# Configuração básica de logging para monitorar o status da aplicação
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação FastAPI.
    Realiza o carregamento do modelo de ML antes da API começar a aceitar requisições.
    """
    # Startup: carrega o modelo antes de aceitar requisições
    logger.info("Iniciando API — carregando modelo...")
    model_module.load_model()
    yield
    # Shutdown (sem ação necessária no momento)
    logger.info("Encerrando API.")


# Inicialização da aplicação FastAPI com metadados configurados
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse, tags=["Monitoramento"])
def health_check():
    """
    Endpoint de verificação de saúde (Health Check).
    Verifica se a API está operacional e se o modelo de machine learning foi carregado corretamente.
    """
    return HealthResponse(
        status="ok",
        model_loaded=model_module.is_model_loaded(),
        version=APP_VERSION,
    )


@app.get("/info", response_model=ModelInfoResponse, tags=["Monitoramento"])
def model_info():
    """
    Retorna informações detalhadas e metadados sobre o modelo.
    Inclui features de entrada, classes de espécies e valores válidos para campos categóricos.
    """
    return ModelInfoResponse(
        version=APP_VERSION,
        species_classes=model_module.get_class_names(),
        input_features=model_module.get_feature_names(),
        valid_islands=["Torgersen", "Biscoe", "Dream"],
        valid_sex_values=["male", "female"],
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Predição"])
def predict(features: PenguinFeatures):
    """
    Endpoint principal para predição.
    Classifica a espécie de um pinguim com base nas características físicas.

    Retorna a espécie predita, confiança e probabilidade por classe.
    """
    try:
        # Chama a lógica de predição encapsulada no módulo do modelo
        result = model_module.predict(features)
    except RuntimeError as exc:
        # Retorna erro 503 se o modelo não estiver disponível ou ocorrer falha na inferência
        raise HTTPException(status_code=503, detail=str(exc))
    return result
