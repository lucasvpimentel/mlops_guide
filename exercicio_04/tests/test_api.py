from fastapi.testclient import TestClient
from app.main import app


def test_api_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_api_info():
    with TestClient(app) as client:
        response = client.get("/info")
        assert response.status_code == 200
        data = response.json()
        assert "metrics" in data
        assert "features" in data


def test_api_predict_success():
    with TestClient(app) as client:
        payload = {
            "age": 45,
            "sex": 0,
            "cp": 1,
            "trestbps": 130,
            "chol": 230,
            "thalach": 170
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "risk_detected" in data
        assert isinstance(data["probability"], float)


def test_api_predict_invalid_data():
    with TestClient(app) as client:
        # Paciente de 150 anos (deve retornar 422)
        payload = {
            "age": 150,
            "sex": 0,
            "cp": 1,
            "trestbps": 130,
            "chol": 230,
            "thalach": 170
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 422
        # Verifica se a mensagem de erro menciona a idade
        assert "age" in response.text
