from typing import Literal
from pydantic import BaseModel, Field, ConfigDict
from app.config import (
    AGE_MIN, AGE_MAX, TRESTBPS_MIN, TRESTBPS_MAX,
    CHOL_MIN, CHOL_MAX, THALACH_MIN, THALACH_MAX
)


class HeartPatientFeatures(BaseModel):
    """Contrato de entrada: Medidas clínicas do paciente."""
    model_config = ConfigDict(extra="forbid")

    age: int = Field(..., ge=AGE_MIN, le=AGE_MAX, description=f"Idade [{AGE_MIN}-{AGE_MAX}]")
    sex: Literal[0, 1] = Field(..., description="Sexo (0=F, 1=M)")
    cp: Literal[0, 1, 2, 3] = Field(..., description="Tipo de dor no peito")
    trestbps: int = Field(
        ..., ge=TRESTBPS_MIN, le=TRESTBPS_MAX,
        description=f"Pressão arterial em repouso [{TRESTBPS_MIN}-{TRESTBPS_MAX}]"
    )
    chol: int = Field(
        ..., ge=CHOL_MIN, le=CHOL_MAX,
        description=f"Colesterol sérico [{CHOL_MIN}-{CHOL_MAX}]"
    )
    thalach: int = Field(
        ..., ge=THALACH_MIN, le=THALACH_MAX,
        description=f"Frequência cardíaca máxima atingida [{THALACH_MIN}-{THALACH_MAX}]"
    )


class HeartRiskResponse(BaseModel):
    """Contrato de saída: Diagnóstico de risco."""
    risk_detected: bool
    probability: float
    model_version: str


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


class ModelInfoResponse(BaseModel):
    version: str
    metrics: dict
    features: list[str]
