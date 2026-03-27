"""
Testes de integração da API FastAPI.

Requerem o modelo treinado em model/penguin_classifier.joblib.
Execute 'python train/train_model.py' antes de rodar estes testes.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID_ADELIE = {
    "bill_length_mm": 39.1,
    "bill_depth_mm": 18.7,
    "flipper_length_mm": 181.0,
    "body_mass_g": 3750.0,
    "island": "Torgersen",
    "sex": "male",
}

VALID_GENTOO = {
    "bill_length_mm": 47.5,
    "bill_depth_mm": 14.2,
    "flipper_length_mm": 209.0,
    "body_mass_g": 5200.0,
    "island": "Biscoe",
    "sex": "female",
}


# --- /health ---

def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200


def test_health_model_loaded():
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "ok"
    assert data["model_loaded"] is True


# --- /info ---

def test_info_returns_200():
    response = client.get("/info")
    assert response.status_code == 200


def test_info_contains_expected_fields():
    response = client.get("/info")
    data = response.json()
    assert "species_classes" in data
    assert "input_features" in data
    assert "Adelie" in data["species_classes"]
    assert "Gentoo" in data["species_classes"]
    assert "Chinstrap" in data["species_classes"]


# --- /predict happy path ---

def test_predict_returns_200_with_valid_input():
    response = client.post("/predict", json=VALID_ADELIE)
    assert response.status_code == 200


def test_predict_response_has_required_fields():
    response = client.post("/predict", json=VALID_ADELIE)
    data = response.json()
    assert "species" in data
    assert "confidence" in data
    assert "probabilities" in data


def test_predict_species_is_valid():
    response = client.post("/predict", json=VALID_ADELIE)
    data = response.json()
    assert data["species"] in ["Adelie", "Chinstrap", "Gentoo"]


def test_predict_confidence_between_0_and_1():
    response = client.post("/predict", json=VALID_ADELIE)
    data = response.json()
    assert 0.0 <= data["confidence"] <= 1.0


def test_predict_probabilities_sum_to_one():
    response = client.post("/predict", json=VALID_ADELIE)
    data = response.json()
    total = sum(data["probabilities"].values())
    assert abs(total - 1.0) < 1e-4


def test_predict_gentoo_features():
    response = client.post("/predict", json=VALID_GENTOO)
    assert response.status_code == 200
    data = response.json()
    assert data["species"] in ["Adelie", "Chinstrap", "Gentoo"]


# --- /predict — validação Pydantic (422) ---

def test_predict_negative_body_mass_returns_422():
    payload = {**VALID_ADELIE, "body_mass_g": -100.0}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_invalid_island_returns_422():
    payload = {**VALID_ADELIE, "island": "Antarctica"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_invalid_sex_returns_422():
    payload = {**VALID_ADELIE, "sex": "unknown"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_empty_body_returns_422():
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_predict_bill_length_out_of_range_returns_422():
    payload = {**VALID_ADELIE, "bill_length_mm": 999.0}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_extra_field_returns_422():
    payload = {**VALID_ADELIE, "extra_field": "not_allowed"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
