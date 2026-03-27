import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    # Garante o startup (carregamento do modelo)
    with TestClient(app) as c:
        yield c


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["model_loaded"] is True


def test_predict_success(client):
    payload = {
        "buying": "vhigh",
        "maint": "vhigh",
        "doors": "2",
        "persons": "2",
        "lug_boot": "small",
        "safety": "low"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert "confidence" in data


def test_predict_invalid_enum(client):
    payload = {
        "buying": "super_high",  # Inválido
        "maint": "vhigh",
        "doors": "2",
        "persons": "2",
        "lug_boot": "small",
        "safety": "low"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
