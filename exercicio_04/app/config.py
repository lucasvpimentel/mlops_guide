from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "heart_model.joblib"

# API Metadata
APP_TITLE = "Heart Disease Diagnosis API"
APP_DESCRIPTION = "API para classificação de risco cardíaco baseada no dataset UCI Heart Disease."
APP_VERSION = "1.0.0"

# Limites Biológicos (Validation Constraints)
AGE_MIN, AGE_MAX = 29, 77
TRESTBPS_MIN, TRESTBPS_MAX = 94, 200
CHOL_MIN, CHOL_MAX = 126, 564
THALACH_MIN, THALACH_MAX = 71, 202

# Enums/Categorias
VALID_SEX = [0, 1] # 0=Female, 1=Male
VALID_CP = [0, 1, 2, 3] # Typical, Atypical, Non-anginal, Asymptomatic
