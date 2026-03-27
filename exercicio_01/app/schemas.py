from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from app.config import (
    BILL_LENGTH_MIN, BILL_LENGTH_MAX,
    BILL_DEPTH_MIN, BILL_DEPTH_MAX,
    FLIPPER_LENGTH_MIN, FLIPPER_LENGTH_MAX,
    BODY_MASS_MIN, BODY_MASS_MAX,
    SPECIES,
)

# Enumerações (Enums) para garantir que apenas valores válidos sejam aceitos
# e para facilitar a integração com a documentação automática.


class Island(str, Enum):
    """Opções válidas para as ilhas do arquipélago Palmer."""
    torgersen = "Torgersen"
    biscoe = "Biscoe"
    dream = "Dream"


class Sex(str, Enum):
    """Opções válidas para o sexo do pinguim."""
    male = "male"
    female = "female"


class PenguinFeatures(BaseModel):
    """
    Contrato de entrada (Request Body).
    Define as medidas físicas necessárias para realizar a predição.
    Cada campo possui validações ge (greater or equal) e le (less or equal).
    """

    # Configura o Pydantic para proibir campos extras no JSON de entrada
    model_config = ConfigDict(extra="forbid")

    bill_length_mm: float = Field(
        ...,
        ge=BILL_LENGTH_MIN,
        le=BILL_LENGTH_MAX,
        description=(
            f"Comprimento do bico em mm "
            f"[{BILL_LENGTH_MIN}, {BILL_LENGTH_MAX}]"
        ),
        examples=[39.1],
    )
    bill_depth_mm: float = Field(
        ...,
        ge=BILL_DEPTH_MIN,
        le=BILL_DEPTH_MAX,
        description=(
            f"Profundidade do bico em mm "
            f"[{BILL_DEPTH_MIN}, {BILL_DEPTH_MAX}]"
        ),
        examples=[18.7],
    )
    flipper_length_mm: float = Field(
        ...,
        ge=FLIPPER_LENGTH_MIN,
        le=FLIPPER_LENGTH_MAX,
        description=(
            f"Comprimento da nadadeira em mm "
            f"[{FLIPPER_LENGTH_MIN}, {FLIPPER_LENGTH_MAX}]"
        ),
        examples=[181.0],
    )
    body_mass_g: float = Field(
        ...,
        ge=BODY_MASS_MIN,
        le=BODY_MASS_MAX,
        description=(
            f"Massa corporal em gramas "
            f"[{BODY_MASS_MIN}, {BODY_MASS_MAX}]"
        ),
        examples=[3750.0],
    )
    island: Island = Field(
        ...,
        description="Ilha onde o pinguim foi observado",
        examples=["Torgersen"],
    )
    sex: Sex = Field(
        ...,
        description="Sexo do pinguim",
        examples=["male"],
    )


class PredictionResponse(BaseModel):
    """
    Contrato de saída (Response Body).
    Retorna o resultado da classificação realizada pelo modelo.
    """

    species: str = Field(
        ...,
        description=f"Espécie predita. Uma de: {SPECIES}"
    )
    confidence: float = Field(
        ...,
        description="Nível de confiança da predição (0.0 a 1.0)"
    )
    probabilities: dict[str, float] = Field(
        ...,
        description=(
            "Probabilidade detalhada para cada uma das espécies possíveis"
        )
    )


class HealthResponse(BaseModel):
    """Esquema para resposta do endpoint de monitoramento /health."""

    status: str
    model_loaded: bool
    version: str


class ModelInfoResponse(BaseModel):
    """Esquema para resposta do endpoint de metadados /info."""

    version: str
    species_classes: list[str]
    input_features: list[str]
    valid_islands: list[str]
    valid_sex_values: list[str]
