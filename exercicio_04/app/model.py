"""
Lógica de inferência para Diagnóstico Cardíaco.
"""
import logging
from typing import Optional
import joblib
import pandas as pd
from app.config import MODEL_PATH
from app.schemas import HeartPatientFeatures, HeartRiskResponse

logger = logging.getLogger(__name__)

_artifact: Optional[dict] = None


def load_model():
    global _artifact
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Arquivo {MODEL_PATH} não encontrado.")
    _artifact = joblib.load(MODEL_PATH)
    logger.info("Modelo de diagnóstico cardíaco carregado.")


def is_model_loaded() -> bool:
    return _artifact is not None


def get_info() -> dict:
    if _artifact is None:
        return {}
    return {
        "version": _artifact["version"],
        "metrics": _artifact["metrics"],
        "features": _artifact["feature_names"]
    }


def predict(features: HeartPatientFeatures) -> HeartRiskResponse:
    if _artifact is None:
        raise RuntimeError("Modelo não carregado.")

    pipeline = _artifact["pipeline"]

    # Criar DataFrame com as features na ordem correta
    X = pd.DataFrame([features.model_dump()])

    # Predição de probabilidade
    prob = pipeline.predict_proba(X)[0][1]  # Probabilidade da classe 1 (doente)
    prediction = bool(prob > 0.5)

    return HeartRiskResponse(
        risk_detected=prediction,
        probability=round(float(prob), 4),
        model_version=_artifact["version"]
    )
