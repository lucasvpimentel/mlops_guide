from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    # Nota: model_loaded dependerá se o treino foi executado antes
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_predict_invalid_data():
    # Payload com valor fora do range UCI (relative_compactness min 0.62)
    bad_payload = {
        "relative_compactness": 0.1, 
        "surface_area_m2": 650.0,
        "wall_area_m2": 300.0,
        "roof_area_m2": 150.0,
        "overall_height_m": 5.0,
        "orientation": 2,
        "glazing_area_pct": 0.25,
        "glazing_area_distribution": 1
    }
    response = client.post("/predict", json=bad_payload)
    assert response.status_code == 422
