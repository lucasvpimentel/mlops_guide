from typing import Literal
from pydantic import BaseModel, Field, ConfigDict
from app.config import (
    RC_MIN, RC_MAX, SA_MIN, SA_MAX, WA_MIN, WA_MAX,
    RA_MIN, RA_MAX, OH_MIN, OH_MAX, VALID_ORIENTATIONS,
    GA_MIN, GA_MAX, VALID_GLAZING_DIST, APP_VERSION
)

class BuildingFeatures(BaseModel):
    """Contrato de entrada: Características físicas do edifício (X1-X8)."""
    model_config = ConfigDict(extra="forbid")

    relative_compactness: float = Field(..., ge=RC_MIN, le=RC_MAX)
    surface_area_m2: float = Field(..., ge=SA_MIN, le=SA_MAX)
    wall_area_m2: float = Field(..., ge=WA_MIN, le=WA_MAX)
    roof_area_m2: float = Field(..., ge=RA_MIN, le=RA_MAX)
    overall_height_m: float = Field(..., ge=OH_MIN, le=OH_MAX)
    orientation: Literal[2, 3, 4, 5] = Field(..., description="2:N, 3:E, 4:S, 5:W")
    glazing_area_pct: float = Field(..., ge=GA_MIN, le=GA_MAX)
    glazing_area_distribution: Literal[0, 1, 2, 3, 4, 5] = Field(...)

class HeatingLoadResponse(BaseModel):
    """Contrato de saída: Previsão de carga de aquecimento."""
    heating_load_kwh: float
    unit: str = "kWh/m²"
    model_version: str = APP_VERSION

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str

class ModelInfoResponse(BaseModel):
    version: str
    algorithm: str = "GradientBoostingRegressor"
    features: list[str]
    target: str = "Heating Load (Y1)"
    metrics: dict[str, float]
