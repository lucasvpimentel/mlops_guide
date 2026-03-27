"""
Gerenciamento do modelo de Machine Learning em memória.

O modelo é carregado uma única vez durante a inicialização (startup) da API
e reutilizado em todas as requisições subsequentes (Singleton Pattern).
"""

import logging
from typing import Optional

import joblib
import numpy as np

from app.config import MODEL_PATH
from app.schemas import DiamondFeatures, PriceResponse

logger = logging.getLogger(__name__)

# Estado global — artefato carregado do disco (Singleton)
_artifact: Optional[dict] = None


def load_model() -> None:
    """
    Lê o arquivo .joblib do disco e mantém o artefato na memória RAM.

    Deve ser chamada uma única vez no startup da API (via lifespan).

    Raises:
        FileNotFoundError: Se o modelo ainda não foi treinado.
    """
    global _artifact

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modelo não encontrado em '{MODEL_PATH}'. "
            "Execute 'python train/train.py' antes de iniciar a API."
        )

    _artifact = joblib.load(MODEL_PATH)
    logger.info(
        "Modelo Diamond Price v%s carregado de '%s'.",
        _artifact.get("version", "?"),
        MODEL_PATH,
    )


def is_model_loaded() -> bool:
    """Retorna True se o artefato está disponível na memória para predição."""
    return _artifact is not None


def get_features() -> list[str]:
    """Retorna os nomes das features registradas no artefato."""
    if _artifact is None:
        return []
    return _artifact.get("features", [])


def get_metrics() -> dict[str, float]:
    """Retorna as métricas de avaliação registradas no treinamento."""
    if _artifact is None:
        return {}
    return _artifact.get("metrics", {})


def get_algorithm() -> str:
    """Retorna o nome do algoritmo de ML usado."""
    if _artifact is None:
        return ""
    return _artifact.get("algorithm", "RandomForestRegressor")


def predict(features: DiamondFeatures) -> PriceResponse:
    """
    Estima o preço do diamante com base nas suas características.

    O pipeline interno (ColumnTransformer + RandomForest) cuida do encoding
    das variáveis categóricas (cut, color, clarity) automaticamente.

    Args:
        features: DiamondFeatures já validado pelo Pydantic

    Returns:
        PriceResponse com preço estimado em USD

    Raises:
        RuntimeError: Se o modelo não foi carregado
    """
    if _artifact is None:
        raise RuntimeError("Modelo não carregado na memória.")

    import pandas as pd

    pipeline = _artifact["pipeline"]

    # Montar DataFrame na ordem das colunas do treino
    X = pd.DataFrame([{
        "carat": features.carat,
        "cut": features.cut,
        "color": features.color,
        "clarity": features.clarity,
        "depth": features.depth,
        "table": features.table,
        "x": features.x,
        "y": features.y,
        "z": features.z,
    }])

    raw_price = pipeline.predict(X)[0]
    price = max(0.0, float(raw_price))  # preço não pode ser negativo

    return PriceResponse(
        price_usd=round(price, 2),
        model_version=_artifact.get("version", "?"),
    )
