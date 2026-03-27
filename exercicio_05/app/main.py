from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from .schemas import CarFeatures, CarPrediction
import joblib
import pandas as pd
import os


# Carregamento do modelo
MODEL_PATH = "models/car_model.joblib"
_model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _model
    if os.path.exists(MODEL_PATH):
        _model = joblib.load(MODEL_PATH)
        print("Modelo de avaliação de carros carregado com sucesso.")
    else:
        print(f"AVISO: Modelo não encontrado em {MODEL_PATH}")
    yield


app = FastAPI(title="Avaliação de Carros — Linter Demo", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": _model is not None}


@app.post("/predict", response_model=CarPrediction)
def predict(features: CarFeatures):
    if _model is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado")

    # Preparar dados para o modelo
    data_dict = features.model_dump()
    data = pd.DataFrame(
        [data_dict.values()],
        columns=data_dict.keys()
    )

    # Predição
    prediction = _model.predict(data)[0]
    probabilities = _model.predict_proba(data)[0]
    confidence = max(probabilities)

    return CarPrediction(label=str(prediction), confidence=float(confidence))
