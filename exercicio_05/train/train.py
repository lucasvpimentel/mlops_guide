"""
Script de treinamento para o Avaliação de Compra de Carros.
Baixa o dataset UCI Car Evaluation (ID: 19) e gera um artefato .joblib.
"""
import sys
from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from ucimlrepo import fetch_ucirepo

# Adiciona raiz ao path para imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "car_model.joblib"

def train():
    print("Buscando dataset Car Evaluation da UCI (ID: 19)...")
    car_evaluation = fetch_ucirepo(id=19)
    
    X = car_evaluation.data.features
    y = car_evaluation.data.targets
    
    # Feature names exatas do UCI
    feature_names = ["buying", "maint", "doors", "persons", "lug_boot", "safety"]
    X.columns = feature_names

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Treinando RandomForestClassifier (N={len(X_train)})...")
    
    # Pipeline com OneHotEncoder para todas as features (todas são categóricas)
    pipeline = Pipeline([
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
        ('clf', RandomForestClassifier(random_state=42, n_estimators=100))
    ])

    pipeline.fit(X_train, y_train.values.ravel())

    # Avaliação
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Acurácia: {acc:.4f}")

    # Artefato serializado
    artifact = {
        "pipeline": pipeline,
        "feature_names": feature_names,
        "metrics": {"accuracy": float(acc)},
        "version": "1.0.0"
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, MODEL_PATH)
    print(f"Modelo serializado com sucesso em: {MODEL_PATH}")

if __name__ == "__main__":
    train()
