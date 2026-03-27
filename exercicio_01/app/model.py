"""
Gerenciamento do modelo de Machine Learning em memória.

O modelo é carregado uma única vez durante a inicialização (startup) da API
e reutilizado em todas as requisições subsequentes (Singleton Pattern).
"""

import logging
from typing import Optional

import joblib
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

from app.config import MODEL_PATH
from app.schemas import PenguinFeatures, PredictionResponse

logger = logging.getLogger(__name__)

# Encoders para variáveis categóricas — essenciais para converter
# texto em números
# Devem seguir rigorosamente a mesma lógica e valores usados durante
# o treinamento.
_ISLAND_ENCODER = LabelEncoder().fit(["Biscoe", "Dream", "Torgersen"])
_SEX_ENCODER = LabelEncoder().fit(["female", "male"])

# Variável de estado para armazenar o artefato do modelo carregado (Singleton)
_artifact: Optional[dict] = None


def load_model() -> None:
    """
    Carrega o arquivo do modelo (.joblib) do disco rígido para a memória RAM.
    Lança um erro explicativo se o modelo ainda não foi treinado.
    """
    global _artifact
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modelo não encontrado em '{MODEL_PATH}'. "
            "Execute 'python train/train_model.py' antes de subir a API."
        )
    # joblib.load recupera o dicionário que contém o Pipeline e os metadados
    _artifact = joblib.load(MODEL_PATH)
    logger.info("Modelo carregado com sucesso de '%s'.", MODEL_PATH)


def is_model_loaded() -> bool:
    """
    Informa se o modelo já está disponível na memória para predição.
    """
    return _artifact is not None


def get_feature_names() -> list[str]:
    """
    Retorna os nomes das features de entrada registradas no artefato
    do modelo.
    """
    if _artifact is None:
        return []
    return _artifact["feature_names"]


def get_class_names() -> list[str]:
    """
    Retorna a lista de nomes das espécies (classes) que o modelo conhece.
    """
    if _artifact is None:
        return []
    return _artifact["class_names"]


def predict(features: PenguinFeatures) -> PredictionResponse:
    """
    Executa o fluxo completo de inferência:
    1. Transforma o objeto de entrada (Pydantic) em um array numérico
       legível pelo modelo.
    2. Aplica as transformações de encoding para campos categóricos.
    3. Chama o Pipeline do Scikit-Learn para calcular as probabilidades.
    4. Formata e retorna o resultado.
    """
    if _artifact is None:
        raise RuntimeError("O modelo ainda não foi carregado pela aplicação.")

    # Recupera o pipeline e as classes do dicionário do modelo
    pipeline: Pipeline = _artifact["pipeline"]
    class_names: list[str] = _artifact["class_names"]

    # Codifica as variáveis categóricas do request em números usando os
    # encoders carregados
    island_encoded = int(
        _ISLAND_ENCODER.transform([features.island.value])[0]
    )
    sex_encoded = int(_SEX_ENCODER.transform([features.sex.value])[0])

    # Monta o array bidimensional de entrada para o Scikit-Learn
    X = np.array([[
        features.bill_length_mm,
        features.bill_depth_mm,
        features.flipper_length_mm,
        features.body_mass_g,
        island_encoded,
        sex_encoded,
    ]])

    # Obtém a probabilidade de cada classe (espécie) para o input fornecido
    probabilities = pipeline.predict_proba(X)[0]
    # Identifica o índice da classe com a maior probabilidade (argmax)
    predicted_index = int(np.argmax(probabilities))
    predicted_species = class_names[predicted_index]
    confidence = float(probabilities[predicted_index])

    # Cria um dicionário mapeando cada espécie para sua probabilidade correspondente
    prob_dict = {cls: round(float(p), 4) for cls, p in zip(class_names, probabilities)}

    return PredictionResponse(
        species=predicted_species,
        confidence=round(confidence, 4),
        probabilities=prob_dict,
    )
