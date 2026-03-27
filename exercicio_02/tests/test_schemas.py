from app.schemas import BuildingFeatures
import pytest
from pydantic import ValidationError


def test_building_features_valid():
    # Happy path com valores médios do dataset
    valid_data = {
        "relative_compactness": 0.75,
        "surface_area_m2": 650.0,
        "wall_area_m2": 300.0,
        "roof_area_m2": 150.0,
        "overall_height_m": 5.0,
        "orientation": 2,
        "glazing_area_pct": 0.25,
        "glazing_area_distribution": 1
    }
    features = BuildingFeatures(**valid_data)
    assert features.relative_compactness == 0.75


def test_building_features_invalid_roof():
    # Roof area não pode ser negativa ou fora do range UCI (110.25 a 220.5)
    with pytest.raises(ValidationError):
        BuildingFeatures(
            relative_compactness=0.75,
            surface_area_m2=650.0,
            wall_area_m2=300.0,
            roof_area_m2=50.0,  # Inválido (min 110.25)
            overall_height_m=5.0,
            orientation=2,
            glazing_area_pct=0.25,
            glazing_area_distribution=1
        )


def test_building_features_invalid_orientation():
    # Orientation só aceita {2,3,4,5}
    with pytest.raises(ValidationError):
        BuildingFeatures(
            relative_compactness=0.75,
            surface_area_m2=650.0,
            wall_area_m2=300.0,
            roof_area_m2=150.0,
            overall_height_m=5.0,
            orientation=9,  # Inválido
            glazing_area_pct=0.25,
            glazing_area_distribution=1
        )


def test_building_features_extra_field():
    # extra="forbid" deve bloquear campos desconhecidos
    with pytest.raises(ValidationError):
        BuildingFeatures(
            relative_compactness=0.75,
            surface_area_m2=650.0,
            wall_area_m2=300.0,
            roof_area_m2=150.0,
            overall_height_m=5.0,
            orientation=2,
            glazing_area_pct=0.25,
            glazing_area_distribution=1,
            unknown_field="hack"
        )
