import pytest
from pydantic import ValidationError
from app.schemas import HeartPatientFeatures

def test_heart_features_happy_path():
    # Dados válidos (dentro dos limites UCI)
    data = {
        "age": 54,
        "sex": 1,
        "cp": 2,
        "trestbps": 120,
        "chol": 240,
        "thalach": 150
    }
    features = HeartPatientFeatures(**data)
    assert features.age == 54

def test_heart_features_invalid_age():
    # Idade impossível (conforme regra do Pydantic)
    with pytest.raises(ValidationError) as exc:
        HeartPatientFeatures(age=150, sex=1, cp=2, trestbps=120, chol=240, thalach=150)
    assert "age" in str(exc.value)

def test_heart_features_negative_age():
    # Idade negativa
    with pytest.raises(ValidationError):
        HeartPatientFeatures(age=-5, sex=1, cp=2, trestbps=120, chol=240, thalach=150)

def test_heart_features_invalid_sex():
    # Sexo deve ser 0 ou 1
    with pytest.raises(ValidationError):
        HeartPatientFeatures(age=50, sex=2, cp=2, trestbps=120, chol=240, thalach=150)

def test_heart_features_invalid_cp():
    # CP deve ser 0, 1, 2 ou 3
    with pytest.raises(ValidationError):
        HeartPatientFeatures(age=50, sex=1, cp=4, trestbps=120, chol=240, thalach=150)

def test_heart_features_extreme_cholesterol():
    # Colesterol muito alto (limite UCI é 564)
    with pytest.raises(ValidationError):
        HeartPatientFeatures(age=50, sex=1, cp=2, trestbps=120, chol=999, thalach=150)

def test_heart_features_extra_field():
    # Campos extras proibidos
    with pytest.raises(ValidationError):
        HeartPatientFeatures(age=50, sex=1, cp=2, trestbps=120, chol=240, thalach=150, weight=80)
