"""
Gerenciamento do modelo de Machine Learning em memória.

O modelo é carregado uma única vez durante o startup da API (Singleton Pattern).

=============================================================================
O "PULO DO GATO": Simetria de Pré-processamento (Training-Serving Symmetry)
=============================================================================

Durante o TREINO:
    imagem 28×28 → achatar → dividir por 255 → array [0, 1]

Durante o SERVING (esta API):
    bytes → PIL → grayscale → resize(28×28) → achatar → dividir por 255 → array [0, 1]

Se essa simetria for quebrada, o modelo recebe dados em distribuição diferente
do treino e as predições serão incorretas ("training-serving skew").
=============================================================================
"""

import io
import logging
from typing import Optional

import joblib
import numpy as np
from PIL import Image

from app.config import CLASSES, IMAGE_SIZE, MODEL_PATH
from app.schemas import FashionPredictionResponse, ImageArrayInput

logger = logging.getLogger(__name__)

_artifact: Optional[dict] = None


def load_model() -> None:
    """
    Lê o arquivo .joblib do disco e mantém o artefato na memória RAM.
    Deve ser chamada uma única vez no startup da API (via lifespan).
    """
    global _artifact

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modelo não encontrado em '{MODEL_PATH}'. "
            "Execute 'python train/train.py' antes de iniciar a API."
        )

    _artifact = joblib.load(MODEL_PATH)
    logger.info(
        "Modelo Fashion MNIST v%s carregado de '%s'.",
        _artifact.get("version", "?"),
        MODEL_PATH,
    )


def is_model_loaded() -> bool:
    return _artifact is not None


def get_model_info() -> dict:
    if _artifact is None:
        return {}
    return {
        "version": _artifact.get("version", "?"),
        "algorithm": _artifact.get("algorithm", "MLPClassifier"),
        "input_shape": _artifact.get("input_shape", f"{IMAGE_SIZE * IMAGE_SIZE}"),
        "classes": _artifact.get("classes", CLASSES),
        "metrics": _artifact.get("metrics", {}),
    }


def preprocess_image_bytes(image_bytes: bytes) -> np.ndarray:
    """
    Converte bytes brutos de uma imagem no array que o modelo espera.

    Pipeline (idêntico ao pré-processamento do treino):
        1. Decodifica bytes → PIL.Image
        2. Converte para escala de cinza (modo "L")
        3. Redimensiona para 28×28
        4. Converte para float32 e normaliza: /255.0 → [0.0, 1.0]
        5. Achata: (28, 28) → (784,)
        6. Adiciona batch: (784,) → (1, 784)
    """
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert("L")
    image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    arr = np.array(image, dtype=np.float32) / 255.0
    return arr.flatten().reshape(1, -1)


def preprocess_array(pixels: list[float]) -> np.ndarray:
    """
    Normaliza um array de pixels já em formato lista Python.
    Aplica a mesma normalização do treino (/255.0).
    """
    arr = np.array(pixels, dtype=np.float32) / 255.0
    return arr.reshape(1, -1)


def _format_prediction(probabilities_arr: np.ndarray) -> FashionPredictionResponse:
    classes: list[str] = _artifact["classes"]  # type: ignore[index]
    predicted_index = int(np.argmax(probabilities_arr))
    confidence = float(probabilities_arr[predicted_index])
    prob_dict = {
        cls: round(float(p), 4)
        for cls, p in zip(classes, probabilities_arr)
    }
    return FashionPredictionResponse(
        category=classes[predicted_index],
        category_index=predicted_index,
        confidence=round(confidence, 4),
        probabilities=prob_dict,
    )


def predict_from_image(image_bytes: bytes) -> FashionPredictionResponse:
    """Classifica a peça de roupa a partir de bytes de uma imagem."""
    if _artifact is None:
        raise RuntimeError("Modelo não carregado na memória.")
    X = preprocess_image_bytes(image_bytes)
    probabilities = _artifact["pipeline"].predict_proba(X)[0]
    return _format_prediction(probabilities)


def predict_from_array(input_data: ImageArrayInput) -> FashionPredictionResponse:
    """Classifica a peça de roupa a partir de um array JSON de pixels."""
    if _artifact is None:
        raise RuntimeError("Modelo não carregado na memória.")
    X = preprocess_array(input_data.pixels)
    probabilities = _artifact["pipeline"].predict_proba(X)[0]
    return _format_prediction(probabilities)
