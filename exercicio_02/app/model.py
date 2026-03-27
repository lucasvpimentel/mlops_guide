"""
Módulo de carregamento e inferência do modelo Energy Efficiency.
O modelo é carregado no startup da API e mantido em memória (Singleton).
"""
import logging
from typing import Optional
import joblib
import numpy as np
from app.config import MODEL_PATH
from app.schemas import BuildingFeatures, HeatingLoadResponse

logger = logging.getLogger(__name__)

# Estado do módulo: Artefato do modelo
_artifact: Optional[dict] = None

def load_model():
    """Lê o arquivo .joblib do disco."""
    global _artifact
    if not MODEL_PATH.exists():
        logger.error(f"Artefato não encontrado em {MODEL_PATH}. API falhará no startup.")
        raise FileNotFoundError("Execute 'python train/train.py' primeiro.")
    
    _artifact = joblib.load(MODEL_PATH)
    logger.info(f"Modelo Energy Efficiency v{_artifact['version']} carregado com sucesso.")

def is_model_loaded() -> bool:
    return _artifact is not None

def get_model_metrics() -> dict:
    return _artifact["metrics"] if _artifact else {}

def get_model_features() -> list[str]:
    return _artifact["features"] if _artifact else []

def predict(features: BuildingFeatures) -> HeatingLoadResponse:
    """Executa a predição usando o pipeline carregado."""
    if _artifact is None:
        raise RuntimeError("Modelo não carregado na memória.")

    pipeline = _artifact["pipeline"]
    
    # Transforma o schema Pydantic em array numpy (ordem das colunas do UCI)
    # X1, X2, X3, X4, X5, X6, X7, X8
    X = np.array([[
        features.relative_compactness,
        features.surface_area_m2,
        features.wall_area_m2,
        features.roof_area_m2,
        features.overall_height_m,
        features.orientation,
        features.glazing_area_pct,
        features.glazing_area_distribution
    ]])

    heating_load = pipeline.predict(X)[0]

    return HeatingLoadResponse(
        heating_load_kwh=round(float(heating_load), 2),
        model_version=_artifact["version"]
    )
