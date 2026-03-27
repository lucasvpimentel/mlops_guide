"""
Testes unitários das validações Pydantic.

Não requerem o modelo treinado — testam apenas os contratos de dados.
"""

import pytest
from pydantic import ValidationError

from app.schemas import PenguinFeatures

VALID_INPUT = {
    "bill_length_mm": 39.1,
    "bill_depth_mm": 18.7,
    "flipper_length_mm": 181.0,
    "body_mass_g": 3750.0,
    "island": "Torgersen",
    "sex": "male",
}


def make(**overrides) -> dict:
    return {**VALID_INPUT, **overrides}


# --- Happy path ---

def test_valid_input_accepted():
    penguin = PenguinFeatures(**VALID_INPUT)
    assert penguin.bill_length_mm == 39.1


def test_boundary_values_accepted():
    """Valores exatamente nos limites devem ser aceitos."""
    penguin = PenguinFeatures(**make(
        bill_length_mm=10.0,
        bill_depth_mm=5.0,
        flipper_length_mm=100.0,
        body_mass_g=500.0,
    ))
    assert penguin.body_mass_g == 500.0


# --- body_mass_g ---

def test_negative_body_mass_rejected():
    with pytest.raises(ValidationError) as exc_info:
        PenguinFeatures(**make(body_mass_g=-100.0))
    assert "body_mass_g" in str(exc_info.value)


def test_zero_body_mass_rejected():
    with pytest.raises(ValidationError):
        PenguinFeatures(**make(body_mass_g=0.0))


def test_body_mass_below_min_rejected():
    with pytest.raises(ValidationError):
        PenguinFeatures(**make(body_mass_g=499.9))


def test_body_mass_above_max_rejected():
    with pytest.raises(ValidationError):
        PenguinFeatures(**make(body_mass_g=10_001.0))


# --- bill_length_mm ---

def test_bill_length_below_min_rejected():
    with pytest.raises(ValidationError) as exc_info:
        PenguinFeatures(**make(bill_length_mm=9.9))
    assert "bill_length_mm" in str(exc_info.value)


def test_bill_length_above_max_rejected():
    with pytest.raises(ValidationError):
        PenguinFeatures(**make(bill_length_mm=80.1))


# --- bill_depth_mm ---

def test_bill_depth_below_min_rejected():
    with pytest.raises(ValidationError):
        PenguinFeatures(**make(bill_depth_mm=4.9))


def test_bill_depth_above_max_rejected():
    with pytest.raises(ValidationError):
        PenguinFeatures(**make(bill_depth_mm=30.1))


# --- flipper_length_mm ---

def test_flipper_length_below_min_rejected():
    with pytest.raises(ValidationError):
        PenguinFeatures(**make(flipper_length_mm=99.9))


def test_flipper_length_above_max_rejected():
    with pytest.raises(ValidationError):
        PenguinFeatures(**make(flipper_length_mm=300.1))


# --- island ---

def test_invalid_island_rejected():
    with pytest.raises(ValidationError) as exc_info:
        PenguinFeatures(**make(island="Antarctica"))
    assert "island" in str(exc_info.value)


def test_all_valid_islands_accepted():
    for island in ["Torgersen", "Biscoe", "Dream"]:
        penguin = PenguinFeatures(**make(island=island))
        assert penguin.island.value == island


# --- sex ---

def test_invalid_sex_rejected():
    with pytest.raises(ValidationError) as exc_info:
        PenguinFeatures(**make(sex="unknown"))
    assert "sex" in str(exc_info.value)


def test_valid_sex_values_accepted():
    for sex in ["male", "female"]:
        penguin = PenguinFeatures(**make(sex=sex))
        assert penguin.sex.value == sex


# --- Extra fields ---

def test_extra_fields_rejected():
    """extra='forbid' — campos desconhecidos devem ser rejeitados."""
    with pytest.raises(ValidationError):
        PenguinFeatures(**make(unknown_field="value"))


# --- Missing fields ---

def test_missing_required_field_rejected():
    data = {k: v for k, v in VALID_INPUT.items() if k != "body_mass_g"}
    with pytest.raises(ValidationError) as exc_info:
        PenguinFeatures(**data)
    assert "body_mass_g" in str(exc_info.value)
