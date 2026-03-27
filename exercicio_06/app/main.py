"""
Aplicação FastAPI — Fashion MNIST Classifier.

Endpoints:
    GET  /health          → Verificação de saúde
    GET  /info            → Metadados do modelo
    POST /predict/upload  → Predição via upload de arquivo de imagem
    POST /predict/array   → Predição via array JSON de pixels
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, HTTPException, UploadFile

from app import model as model_module
from app.config import ALLOWED_CONTENT_TYPES, APP_DESCRIPTION, APP_TITLE, APP_VERSION
from app.schemas import (
    FashionPredictionResponse,
    HealthResponse,
    ImageArrayInput,
    ModelInfoResponse,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carrega o modelo antes de aceitar requisições; libera ao encerrar."""
    logger.info("Iniciando API — carregando modelo Fashion MNIST...")
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


@app.get("/info", response_model=ModelInfoResponse, tags=["Monitoramento"])
def model_info():
    """Retorna metadados do modelo carregado (algoritmo, classes, métricas)."""
    if not model_module.is_model_loaded():
        raise HTTPException(status_code=503, detail="Modelo não disponível.")
    info = model_module.get_model_info()
    return ModelInfoResponse(
        version=info["version"],
        algorithm=info["algorithm"],
        input_shape=info["input_shape"],
        n_classes=len(info["classes"]),
        classes=info["classes"],
        metrics=info["metrics"],
    )


@app.post("/predict/upload", response_model=FashionPredictionResponse, tags=["Predição"])
async def predict_from_upload(file: UploadFile = File(...)):
    """
    Recebe uma imagem (JPEG/PNG/WebP/BMP) e classifica a peça de roupa.

    A imagem é automaticamente convertida para 28×28 grayscale internamente.
    Não é necessário pré-processar a imagem antes de enviar.
    """
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=(
                f"Tipo de arquivo não suportado: '{file.content_type}'. "
                f"Use: {sorted(ALLOWED_CONTENT_TYPES)}"
            ),
        )

    image_bytes = await file.read()

    try:
        result = model_module.predict_from_image(image_bytes)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        logger.error("Erro ao processar imagem '%s': %s", file.filename, exc)
        raise HTTPException(
            status_code=422,
            detail=f"Imagem inválida ou corrompida: {exc}",
        )

    return result


@app.post("/predict/array", response_model=FashionPredictionResponse, tags=["Predição"])
def predict_from_array(input_data: ImageArrayInput):
    """
    Recebe um array JSON de 784 valores de pixel [0, 255] e classifica a peça de roupa.

    Alternativa programática ao upload de arquivo — ideal para notebooks e scripts.
    """
    try:
        return model_module.predict_from_array(input_data)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
