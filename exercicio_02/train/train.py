"""
Script de treinamento único para o modelo de Eficiência Energética.
Serializa o artefato em model/modelo_energia.joblib.
"""
import sys
from pathlib import Path
import joblib
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import root_mean_squared_error, r2_score
from ucimlrepo import fetch_ucirepo

# Adiciona raiz ao path para imports de app.config
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.config import MODEL_PATH, APP_VERSION

def train():
    print("Buscando dataset Energy Efficiency (UCI ID: 242)...")
    energy_efficiency = fetch_ucirepo(id=242)
    
    X = energy_efficiency.data.features
    y = energy_efficiency.data.targets['Y1'] # Heating Load

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Treinando GradientBoostingRegressor (N={len(X_train)})...")
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', GradientBoostingRegressor(random_state=42))
    ])

    pipeline.fit(X_train, y_train)

    # Avaliação
    y_pred = pipeline.predict(X_test)
    rmse = root_mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Métricas: RMSE={rmse:.4f}, R²={r2:.4f}")

    # Artefato serializado
    artifact = {
        "pipeline": pipeline,
        "features": list(X.columns),
        "metrics": {"rmse": float(rmse), "r2": float(r2)},
        "version": APP_VERSION
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, MODEL_PATH)
    print(f"Modelo serializado com sucesso em: {MODEL_PATH}")

if __name__ == "__main__":
    train()
