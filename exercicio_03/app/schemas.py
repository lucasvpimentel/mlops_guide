"""
Schemas Pydantic para validação de dados da API.

Define os contratos de entrada e saída de todos os endpoints.
A validação acontece automaticamente antes de qualquer lógica de negócio.
"""

from typing import Literal

from pydantic import BaseModel, Field, ConfigDict

from app.config import (
    APP_VERSION,
    CARAT_MIN, CARAT_MAX,
    DEPTH_MIN, DEPTH_MAX,
    TABLE_MIN, TABLE_MAX,
    X_MIN, X_MAX,
    Y_MIN, Y_MAX,
    Z_MIN, Z_MAX,
    VALID_CUTS,
    VALID_COLORS,
    VALID_CLARITIES,
)


# ---------------------------------------------------------------------------
# Schema de entrada (Request)
# ---------------------------------------------------------------------------


class DiamondFeatures(BaseModel):
    """
    Características de um diamante para estimativa de preço.

    Todas as features são validadas com os limites do dataset original.
    Campos extras são rejeitados automaticamente (extra='forbid').
    """

    model_config = ConfigDict(extra="forbid")

    carat: float = Field(
        ...,
        ge=CARAT_MIN,
        le=CARAT_MAX,
        description=f"Peso do diamante em quilates [{CARAT_MIN}, {CARAT_MAX}]",
        examples=[0.89],
    )
    cut: Literal["Fair", "Good", "Very Good", "Premium", "Ideal"] = Field(
        ...,
        description=f"Qualidade do corte. Uma de: {VALID_CUTS}",
        examples=["Ideal"],
    )
    color: Literal["D", "E", "F", "G", "H", "I", "J"] = Field(
        ...,
        description=f"Cor do diamante. Uma de: {VALID_COLORS} (D = melhor, J = pior)",
        examples=["E"],
    )
    clarity: Literal["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2", "I1"] = Field(
        ...,
        description=f"Clareza do diamante. Uma de: {VALID_CLARITIES} (IF = melhor, I1 = pior)",
        examples=["VS1"],
    )
    depth: float = Field(
        ...,
        ge=DEPTH_MIN,
        le=DEPTH_MAX,
        description=f"Profundidade total (%) [{DEPTH_MIN}, {DEPTH_MAX}]",
        examples=[62.3],
    )
    table: float = Field(
        ...,
        ge=TABLE_MIN,
        le=TABLE_MAX,
        description=f"Largura do topo em relação ao ponto mais largo (%) [{TABLE_MIN}, {TABLE_MAX}]",
        examples=[57.0],
    )
    x: float = Field(
        ...,
        ge=X_MIN,
        le=X_MAX,
        description=f"Comprimento em mm [{X_MIN}, {X_MAX}]",
        examples=[6.18],
    )
    y: float = Field(
        ...,
        ge=Y_MIN,
        le=Y_MAX,
        description=f"Largura em mm [{Y_MIN}, {Y_MAX}]",
        examples=[6.21],
    )
    z: float = Field(
        ...,
        ge=Z_MIN,
        le=Z_MAX,
        description=f"Profundidade em mm [{Z_MIN}, {Z_MAX}]",
        examples=[3.86],
    )


# ---------------------------------------------------------------------------
# Schemas de saída (Response)
# ---------------------------------------------------------------------------


class PriceResponse(BaseModel):
    """Resposta da predição com preço estimado em USD."""

    price_usd: float = Field(
        ...,
        description="Preço estimado do diamante em dólares americanos (USD)",
        examples=[4500.00],
    )
    model_version: str = Field(
        ...,
        description="Versão do modelo que gerou a predição",
        examples=[APP_VERSION],
    )


class HealthResponse(BaseModel):
    """Resposta do endpoint de verificação de saúde da API."""

    status: str = Field(..., examples=["ok"])
    model_loaded: bool = Field(..., description="True se o modelo está carregado na memória")
    version: str = Field(..., examples=[APP_VERSION])


class ModelInfoResponse(BaseModel):
    """Metadados do modelo carregado: algoritmo, features e métricas."""

    version: str
    algorithm: str = Field(..., examples=["RandomForestRegressor"])
    features: list[str]
    target: str = Field(..., examples=["price (USD)"])
    metrics: dict[str, float]
