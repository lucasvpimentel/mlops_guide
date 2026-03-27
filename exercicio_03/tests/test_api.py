"""
Testes de integração para os endpoints FastAPI.
Requerem o modelo treinado em model/diamond_price_model.joblib.
Execute 'python train/train.py' antes de rodar estes testes.
"""

import pytest
from fastapi.testclient import TestClient


from app.main import app

VALID_PAYLOAD = {
    "carat": 0.89,
    "cut": "Ideal",
    "color": "E",
    "clarity": "VS1",
    "depth": 62.3,
    "table": 57.0,
    "x": 6.18,
    "y": 6.21,
    "z": 3.86,
}


@pytest.fixture(scope="module")
def client():
    """Inicia o lifespan da API (carrega o modelo) antes dos testes."""
    with TestClient(app) as c:
        yield c


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        assert client.get("/health").status_code == 200

    def test_health_model_loaded(self, client):
        assert client.get("/health").json()["model_loaded"] is True

    def test_health_status_ok(self, client):
        assert client.get("/health").json()["status"] == "ok"


class TestInfoEndpoint:
    def test_info_returns_200(self, client):
        assert client.get("/info").status_code == 200

    def test_info_has_9_features(self, client):
        assert len(client.get("/info").json()["features"]) == 9

    def test_info_has_metrics(self, client):
        data = client.get("/info").json()
        assert "rmse" in data["metrics"]
        assert "r2" in data["metrics"]


class TestPredictEndpoint:
    def test_valid_input_returns_200(self, client):
        assert client.post("/predict", json=VALID_PAYLOAD).status_code == 200

    def test_returns_positive_price(self, client):
        data = client.post("/predict", json=VALID_PAYLOAD).json()
        assert data["price_usd"] > 0

    def test_returns_model_version(self, client):
        data = client.post("/predict", json=VALID_PAYLOAD).json()
        assert "model_version" in data

    def test_invalid_cut_returns_422(self, client):
        payload = {**VALID_PAYLOAD, "cut": "Perfeito"}
        assert client.post("/predict", json=payload).status_code == 422

    def test_invalid_color_returns_422(self, client):
        payload = {**VALID_PAYLOAD, "color": "Z"}
        assert client.post("/predict", json=payload).status_code == 422

    def test_carat_out_of_range_returns_422(self, client):
        payload = {**VALID_PAYLOAD, "carat": 99.0}
        assert client.post("/predict", json=payload).status_code == 422

    def test_extra_field_returns_422(self, client):
        payload = {**VALID_PAYLOAD, "extra": "campo"}
        assert client.post("/predict", json=payload).status_code == 422

    def test_fair_cut_returns_lower_price_than_ideal(self, client):
        """Diamante com corte Fair deve custar menos que corte Ideal."""
        ideal = client.post("/predict", json={**VALID_PAYLOAD, "cut": "Ideal"}).json()
        fair = client.post("/predict", json={**VALID_PAYLOAD, "cut": "Fair"}).json()
        assert ideal["price_usd"] >= fair["price_usd"]
