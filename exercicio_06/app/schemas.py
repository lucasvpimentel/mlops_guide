"""
Schemas Pydantic para validação de dados da API.
A validação acontece automaticamente antes de qualquer lógica de negócio.
"""

from pydantic import BaseModel, Field, ConfigDict

from app.config import APP_VERSION, CLASSES, N_PIXELS


class ImageArrayInput(BaseModel):
    """
    Entrada alternativa: lista de 784 valores de pixel em formato JSON.
    Útil para uso programático sem necessidade de criar um arquivo de imagem.
    Cada valor representa a intensidade de um pixel em escala de cinza [0, 255].
    """

    model_config = ConfigDict(extra="forbid")

    pixels: list[float] = Field(
        ...,
        min_length=N_PIXELS,
        max_length=N_PIXELS,
        description=(
            f"Lista de exatamente {N_PIXELS} valores de pixel [0, 255]. "
            "Representa uma imagem 28×28 em escala de cinza, linearizada por linha."
        ),
        examples=[[128.0] * N_PIXELS],
    )


class FashionPredictionResponse(BaseModel):
    """Resposta da predição com categoria, confiança e distribuição de probabilidades."""

    category: str = Field(
        ...,
        description=f"Categoria predita. Uma de: {CLASSES}",
        examples=["Camiseta/Top"],
    )
    category_index: int = Field(
        ...,
        ge=0,
        le=9,
        description="Índice numérico da categoria (0 a 9)",
        examples=[0],
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confiança da predição principal (0.0 a 1.0)",
        examples=[0.92],
    )
    probabilities: dict[str, float] = Field(
        ...,
        description="Probabilidade para cada uma das 10 categorias (soma = 1.0)",
    )


class HealthResponse(BaseModel):
    """Resposta do endpoint de verificação de saúde da API."""

    status: str = Field(..., examples=["ok"])
    model_loaded: bool = Field(..., description="True se o modelo está na memória")
    version: str = Field(..., examples=[APP_VERSION])


class ModelInfoResponse(BaseModel):
    """Metadados do modelo carregado."""

    version: str
    algorithm: str = Field(..., examples=["MLPClassifier"])
    input_shape: str = Field(..., examples=["784 (28x28 grayscale, normalizado [0,1])"])
    n_classes: int = Field(..., examples=[10])
    classes: list[str]
    metrics: dict[str, float]
