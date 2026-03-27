"""
Script de treinamento para o Diagnóstico de Saúde do Coração.
Baixa o dataset UCI Heart Disease (ID: 45) e gera um artefato .joblib.
"""
import sys
from pathlib import Path
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from ucimlrepo import fetch_ucirepo

# Adiciona raiz ao path para permitir imports de app.config futuramente se necessário
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "heart_model.joblib"

def train():
    print("Buscando dataset Heart Disease da UCI (ID: 45)...")
    heart_disease = fetch_ucirepo(id=45)
    
    X = heart_disease.data.features
    # O target 'num' varia de 0 (saudável) a 4 (doente). 
    # Vamos binarizar: 0 vs (1,2,3,4)
    y = (heart_disease.data.targets['num'] > 0).astype(int)

    # Selecionar apenas as colunas principais para simplificar o exercício e os testes
    # Age, Sex, CP, Trestbps, Chol, Thalach
    cols_to_use = ['age', 'sex', 'cp', 'trestbps', 'chol', 'thalach']
    X = X[cols_to_use]

    # Remover nulos (o dataset UCI tem alguns '?' que o ucimlrepo converte para NaN)
    X = X.fillna(X.median())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Treinando RandomForestClassifier (N={len(X_train)})...")
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', RandomForestClassifier(random_state=42, n_estimators=100))
    ])

    pipeline.fit(X_train, y_train)

    # Avaliação
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Acurácia: {acc:.4f}")
    print("\nRelatório de Classificação:")
    print(classification_report(y_test, y_pred))

    # Artefato serializado
    artifact = {
        "pipeline": pipeline,
        "feature_names": cols_to_use,
        "metrics": {"accuracy": float(acc)},
        "version": "1.0.0"
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, MODEL_PATH)
    print(f"Modelo serializado com sucesso em: {MODEL_PATH}")

if __name__ == "__main__":
    train()
