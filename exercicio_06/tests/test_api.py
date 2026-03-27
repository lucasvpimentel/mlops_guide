"""
Testes de integração para os endpoints FastAPI.

Requerem o modelo treinado em model/fashion_classifier.joblib.
Execute 'python train/train.py' antes de rodar estes testes.
"""

import io

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app

client = TestClient(app)


def create_synthetic_png(size: tuple[int, int] = (28, 28)) -> bytes:
    """Cria um PNG sintético em memória para testes de upload."""
    # Imagem grayscale com padrão simples
    data = np.random.randint(0, 256, (size[1], size[0]), dtype=np.uint8)
    img = Image.fromarray(data, mode="L")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


VALID_ARRAY_PAYLOAD = {"pixels": [128.0] * 784}


# ---------------------------------------------------------------------------
# Testes de monitoramento
# ---------------------------------------------------------------------------


class TestHealthEndpoint:
    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_model_loaded(self):
        data = response = client.get("/health").json()
        assert data["model_loaded"] is True

    def test_health_has_version(self):
        data = client.get("/health").json()
        assert "version" in data
        assert data["status"] == "ok"


class TestInfoEndpoint:
    def test_info_returns_200(self):
        response = client.get("/info")
        assert response.status_code == 200

    def test_info_has_10_classes(self):
        data = client.get("/info").json()
        assert data["n_classes"] == 10

    def test_info_has_metrics(self):
        data = client.get("/info").json()
        assert "metrics" in data
        assert "accuracy" in data["metrics"]

    def test_info_classes_count(self):
        data = client.get("/info").json()
        assert len(data["classes"]) == 10


# ---------------------------------------------------------------------------
# Testes de predição via upload
# ---------------------------------------------------------------------------


class TestPredictUploadEndpoint:
    def test_upload_valid_png_returns_200(self):
        png_bytes = create_synthetic_png()
        response = client.post(
            "/predict/upload",
            files={"file": ("test.png", png_bytes, "image/png")},
        )
        assert response.status_code == 200

    def test_upload_returns_valid_category_index(self):
        png_bytes = create_synthetic_png()
        data = client.post(
            "/predict/upload",
            files={"file": ("test.png", png_bytes, "image/png")},
        ).json()
        assert 0 <= data["category_index"] <= 9

    def test_upload_returns_confidence_in_range(self):
        png_bytes = create_synthetic_png()
        data = client.post(
            "/predict/upload",
            files={"file": ("test.png", png_bytes, "image/png")},
        ).json()
        assert 0.0 <= data["confidence"] <= 1.0

    def test_upload_probabilities_sum_to_one(self):
        png_bytes = create_synthetic_png()
        data = client.post(
            "/predict/upload",
            files={"file": ("test.png", png_bytes, "image/png")},
        ).json()
        total = sum(data["probabilities"].values())
        assert abs(total - 1.0) < 1e-3

    def test_upload_probabilities_has_10_entries(self):
        png_bytes = create_synthetic_png()
        data = client.post(
            "/predict/upload",
            files={"file": ("test.png", png_bytes, "image/png")},
        ).json()
        assert len(data["probabilities"]) == 10

    def test_upload_large_image_returns_200(self):
        """Imagem grande deve ser redimensionada automaticamente."""
        png_bytes = create_synthetic_png(size=(256, 256))
        response = client.post(
            "/predict/upload",
            files={"file": ("big.png", png_bytes, "image/png")},
        )
        assert response.status_code == 200

    def test_upload_unsupported_type_returns_415(self):
        """Arquivo de texto deve retornar 415 Unsupported Media Type."""
        response = client.post(
            "/predict/upload",
            files={"file": ("data.txt", b"hello world", "text/plain")},
        )
        assert response.status_code == 415

    def test_upload_pdf_returns_415(self):
        response = client.post(
            "/predict/upload",
            files={"file": ("doc.pdf", b"%PDF-1.4", "application/pdf")},
        )
        assert response.status_code == 415


# ---------------------------------------------------------------------------
# Testes de predição via array JSON
# ---------------------------------------------------------------------------


class TestPredictArrayEndpoint:
    def test_array_784_zeros_returns_200(self):
        response = client.post("/predict/array", json={"pixels": [0.0] * 784})
        assert response.status_code == 200

    def test_array_784_values_returns_valid_response(self):
        data = client.post("/predict/array", json=VALID_ARRAY_PAYLOAD).json()
        assert 0 <= data["category_index"] <= 9
        assert 0.0 <= data["confidence"] <= 1.0

    def test_array_probabilities_sum_to_one(self):
        data = client.post("/predict/array", json=VALID_ARRAY_PAYLOAD).json()
        total = sum(data["probabilities"].values())
        assert abs(total - 1.0) < 1e-3

    def test_array_783_pixels_returns_422(self):
        """Array incompleto deve retornar 422."""
        response = client.post("/predict/array", json={"pixels": [128.0] * 783})
        assert response.status_code == 422

    def test_array_785_pixels_returns_422(self):
        """Array com pixels a mais deve retornar 422."""
        response = client.post("/predict/array", json={"pixels": [128.0] * 785})
        assert response.status_code == 422

    def test_array_empty_returns_422(self):
        response = client.post("/predict/array", json={"pixels": []})
        assert response.status_code == 422

    def test_array_extra_field_returns_422(self):
        response = client.post(
            "/predict/array",
            json={"pixels": [128.0] * 784, "extra": "não permitido"},
        )
        assert response.status_code == 422
