import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["model_loaded"] is True


def test_predict_spam(client):
    payload = {"message": "WINNER! You have won a 1000 prize. Call 09061701461 to claim."}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "spam"
    assert data["probability"] > 0.5


def test_predict_ham(client):
    payload = {"message": "Hey, are we still going to the cinema tonight?"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "ham"
    assert data["probability"] < 0.5


def test_predict_invalid_input(client):
    payload = {"message": ""}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
