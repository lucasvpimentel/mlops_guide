"""
model_loader.py
---------------
Responsabilidade única: carregar o artefato treinado do disco e
expor uma função de predição limpa para a camada HTTP.

Padrão Singleton via variável de módulo (_model):
- O modelo é carregado UMA vez quando o servidor inicia.
- Requisições subsequentes reutilizam o objeto em memória.
- Evita latência de I/O por requisição.
"""

import pathlib
from typing import Optional

import joblib
from sklearn.pipeline import Pipeline

from src.preprocessing import clean_text

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model.joblib"

# Variável de módulo — populada uma vez em load_model()
_model: Optional[Pipeline] = None


def load_model() -> None:
    """
    Carrega model.joblib na memória e armazena no singleton _model.
    Chamada no evento de startup do FastAPI (lifespan).
    Levanta FileNotFoundError se o artefato não existir — falha rápida e clara.
    """
    global _model
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Artefato não encontrado: {MODEL_PATH}\n"
            "Execute 'python -m src.train' antes de iniciar a API."
        )
    _model = joblib.load(MODEL_PATH)


def predict(text: str) -> dict:
    """
    Recebe texto bruto, aplica clean_text e retorna predição.

    Retorna:
        {"label": "spam" | "ham", "probability": float}

    IMPORTANTE: clean_text é aplicado aqui com a mesma lógica do treino.
    Se alguém alterar preprocessing.py, os testes unitários quebram antes
    de chegar neste ponto.
    """
    if _model is None:
        raise RuntimeError("Modelo não carregado. Chame load_model() primeiro.")

    cleaned = clean_text(text)
    # predict_proba retorna [[prob_ham, prob_spam]]
    proba = _model.predict_proba([cleaned])[0]
    spam_prob = float(proba[1])
    label = "spam" if spam_prob >= 0.5 else "ham"

    return {"label": label, "probability": round(spam_prob, 4)}
