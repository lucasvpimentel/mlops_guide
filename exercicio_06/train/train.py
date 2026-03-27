"""
Script de treinamento do classificador Fashion MNIST.

Fluxo:
    1. Baixa o dataset Fashion MNIST via tensorflow.keras (60.000 treino / 10.000 teste)
    2. Normaliza e achata as imagens: (28, 28) → (784,) com valores em [0, 1]
    3. Treina um MLPClassifier (sklearn) — sem GPU necessária
    4. Avalia no conjunto de teste
    5. Salva artefato .joblib com pipeline + metadados

Nota: tensorflow é usado APENAS para baixar os dados.
      O modelo salvo (joblib) NÃO depende de tensorflow para servir.

Execução:
    cd exercicio_06/
    python train/train.py
"""

import sys
from pathlib import Path

# Permite importar app.config quando executado a partir da raiz do projeto
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib
import numpy as np
from sklearn.metrics import accuracy_score, classification_report
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline

from app.config import APP_VERSION, CLASSES, MODEL_PATH


def load_fashion_mnist() -> tuple:
    """
    Baixa o Fashion MNIST via tensorflow.keras e prepara os arrays.

    Pré-processamento (deve ser idêntico ao preprocess_image_bytes em model.py):
        - Reshape: (N, 28, 28) → (N, 784)
        - Normalização: uint8 [0, 255] → float32 [0.0, 1.0]

    Returns:
        (X_train, y_train, X_test, y_test) como arrays numpy
    """
    print("Baixando Fashion MNIST via tensorflow.keras...")
    from tensorflow.keras.datasets import fashion_mnist  # type: ignore

    (X_train_raw, y_train), (X_test_raw, y_test) = fashion_mnist.load_data()

    print(f"  Imagens de treino: {X_train_raw.shape}  |  Teste: {X_test_raw.shape}")

    # Achatar e normalizar — MESMA lógica de preprocess_image_bytes() em model.py
    X_train = X_train_raw.reshape(-1, 784).astype(np.float32) / 255.0
    X_test = X_test_raw.reshape(-1, 784).astype(np.float32) / 255.0

    return X_train, y_train, X_test, y_test


def build_pipeline() -> Pipeline:
    """
    Cria o pipeline sklearn: MLPClassifier.

    MLPClassifier com 2 camadas ocultas (256 → 128 neurônios).
    Acurácia esperada no Fashion MNIST: ~87-88%.
    """
    return Pipeline([
        (
            "clf",
            MLPClassifier(
                hidden_layer_sizes=(256, 128),
                max_iter=30,
                random_state=42,
                verbose=True,
                early_stopping=True,   # Para se não melhorar por 10 épocas
                validation_fraction=0.1,
            ),
        )
    ])


def evaluate(pipeline: Pipeline, X_test: np.ndarray, y_test: np.ndarray) -> dict:
    """Avalia o modelo e retorna métricas."""
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nAcurácia no conjunto de teste: {accuracy:.4f} ({accuracy * 100:.1f}%)")
    print("\nRelatório por classe:")
    print(classification_report(y_test, y_pred, target_names=CLASSES))

    return {"accuracy": round(float(accuracy), 4)}


def save_artifact(pipeline: Pipeline, metrics: dict) -> None:
    """Serializa o pipeline e metadados como artefato .joblib."""
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    artifact = {
        "pipeline": pipeline,
        "classes": CLASSES,
        "algorithm": "MLPClassifier",
        "metrics": metrics,
        "version": APP_VERSION,
        "input_shape": "784 (28x28 grayscale, normalizado [0,1])",
    }

    joblib.dump(artifact, MODEL_PATH)
    print(f"\nModelo salvo em: {MODEL_PATH}")


def main() -> None:
    print("=" * 60)
    print("  Fashion MNIST Classifier — Treinamento")
    print("=" * 60)

    X_train, y_train, X_test, y_test = load_fashion_mnist()

    print(f"\nTreinando MLPClassifier (hidden_layers=[256, 128], max_iter=30)...")
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    metrics = evaluate(pipeline, X_test, y_test)
    save_artifact(pipeline, metrics)

    print("\nTreinamento concluído com sucesso.")


if __name__ == "__main__":
    main()
