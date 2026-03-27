"""
Script de treinamento do modelo Diamond Price Predictor.

Fluxo:
    1. Carrega o dataset 'diamonds' via seaborn (53.940 registros)
    2. Usa todas as 9 features (carat, cut, color, clarity, depth, table,
       x, y, z)
    3. Aplica ColumnTransformer: OrdinalEncoder nas categóricas,
       passthrough nas numéricas
    4. Treina um RandomForestRegressor
    5. Avalia com RMSE e R² no conjunto de teste (20%)
    6. Salva artefato .joblib com pipeline + metadados

Execução:
    cd exercicio_03/
    python train/train.py
"""

import sys
from pathlib import Path

# Permite importar app.config quando executado a partir da raiz do projeto
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib  # noqa: E402
import seaborn as sns  # noqa: E402
from sklearn.compose import ColumnTransformer  # noqa: E402
from sklearn.ensemble import RandomForestRegressor  # noqa: E402
from sklearn.metrics import mean_squared_error, r2_score  # noqa: E402
from sklearn.model_selection import train_test_split  # noqa: E402
from sklearn.pipeline import Pipeline  # noqa: E402
from sklearn.preprocessing import OrdinalEncoder  # noqa: E402

from app.config import (  # noqa: E402
    APP_VERSION,
    MODEL_PATH,
)

# Colunas do dataset
CATEGORICAL_FEATURES = ["cut", "color", "clarity"]
NUMERICAL_FEATURES = ["carat", "depth", "table", "x", "y", "z"]
ALL_FEATURES = [
    "carat", "cut", "color", "clarity", "depth", "table", "x", "y", "z"
]
TARGET = "price"


def load_data():
    """Carrega e limpa o dataset diamonds do seaborn."""
    print("Carregando dataset 'diamonds' do seaborn...")
    df = sns.load_dataset("diamonds")
    print(f"  Registros totais: {len(df)}")

    # Remove valores nulos (o dataset é limpo, mas boa prática)
    df = df.dropna(subset=ALL_FEATURES + [TARGET])
    print(f"  Registros após limpeza: {len(df)}")

    X = df[ALL_FEATURES]
    y = df[TARGET]
    return X, y


def build_pipeline() -> Pipeline:
    """
    Cria o pipeline de pré-processamento + modelo.

    OrdinalEncoder para categóricas (cut, color, clarity) — preserva
    a ordem natural das categorias que tem significado de qualidade.
    """
    # Ordens naturais das categorias (da pior para a melhor qualidade)
    cut_order = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
    color_order = ["J", "I", "H", "G", "F", "E", "D"]      # J=pior, D=melhor
    clarity_order = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                OrdinalEncoder(
                    categories=[cut_order, color_order, clarity_order]
                ),
                CATEGORICAL_FEATURES,
            )
        ],
        remainder="passthrough",  # passa numéricas sem transformação
    )

    return Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1,  # usa todos os CPUs disponíveis
        )),
    ])


def evaluate(pipeline: Pipeline, X_test, y_test) -> dict:
    """Avalia o modelo no conjunto de teste e retorna métricas."""
    y_pred = pipeline.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    r2 = r2_score(y_test, y_pred)

    print(f"\nMétricas no conjunto de teste ({len(X_test)} amostras):")
    print(f"  RMSE: {rmse:.2f} USD")
    print(f"  R²:   {r2:.4f}")

    return {"rmse": round(float(rmse), 2), "r2": round(float(r2), 4)}


def save_artifact(pipeline: Pipeline, metrics: dict) -> None:
    """Serializa o pipeline e metadados como artefato .joblib."""
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    artifact = {
        "pipeline": pipeline,
        "features": ALL_FEATURES,
        "algorithm": "RandomForestRegressor",
        "metrics": metrics,
        "version": APP_VERSION,
    }

    joblib.dump(artifact, MODEL_PATH)
    print(f"\nModelo salvo em: {MODEL_PATH}")


def main() -> None:
    print("=" * 60)
    print("  Diamond Price Predictor — Treinamento")
    print("=" * 60)

    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"\n  Treino: {len(X_train)} amostras | Teste: {len(X_test)} amostras")

    print("\nTreinando RandomForestRegressor...")
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    metrics = evaluate(pipeline, X_test, y_test)
    save_artifact(pipeline, metrics)

    print("\nTreinamento concluído com sucesso.")


if __name__ == "__main__":
    main()
