"""
main.py
-------
Camada HTTP da aplicação. Define os endpoints e delega toda lógica
de negócio para app/model_loader.py.

Separação de responsabilidades:
- main.py     → receber requisição, validar schema, devolver resposta
- model_loader → carregar modelo, aplicar preprocessing, inferir
- preprocessing → limpar texto (testável isoladamente)
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app import model_loader


# ---------------------------------------------------------------------------
# Schemas Pydantic — validação automática de entrada e saída
# ---------------------------------------------------------------------------

class PredictRequest(BaseModel):
    """Corpo da requisição POST /predict."""
    # Field com min_length garante que string vazia retorna 422, não 500
    message: str = Field(..., min_length=1, description="Texto SMS a classificar")


class PredictResponse(BaseModel):
    """Corpo da resposta de /predict."""
    label: str = Field(..., description="'spam' ou 'ham'")
    probability: float = Field(..., description="Probabilidade de ser spam (0.0 a 1.0)")


# ---------------------------------------------------------------------------
# Lifespan — executa código na inicialização e no encerramento do servidor
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Carrega o modelo uma vez quando o uvicorn sobe.
    Se model.joblib não existir, o servidor falha com mensagem clara
    em vez de estourar com KeyError na primeira requisição.
    """
    model_loader.load_model()
    yield
    # Espaço para limpeza no shutdown (conexões, threads) — não necessário aqui


# ---------------------------------------------------------------------------
# Aplicação
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Spam Detection API",
    description="Classifica mensagens SMS como spam ou ham usando Naive Bayes.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["infra"])
def health_check():
    """
    Liveness probe — usado pelo Docker e pelo pipeline de CI para confirmar
    que o servidor está de pé e o modelo foi carregado com sucesso.
    """
    return {"status": "ok", "model_loaded": model_loader._model is not None}


@app.post("/predict", response_model=PredictResponse, tags=["inference"])
def predict(request: PredictRequest):
    """
    Classifica uma mensagem SMS.

    - Retorna 200 com label e probabilidade de spam.
    - Retorna 422 se o corpo for inválido (campo ausente, string vazia).
    - Retorna 500 se o modelo não estiver carregado (não deveria ocorrer
      em operação normal, pois o lifespan garante o carregamento).
    """
    try:
        result = model_loader.predict(request.message)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return PredictResponse(**result)
