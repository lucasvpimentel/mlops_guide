"""
Script de treinamento do classificador Fashion MNIST.

Fluxo:
    1. Baixa o dataset Fashion MNIST via tensorflow.keras
       (60.000 treino / 10.000 teste)
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

import joblib  # noqa: E402
from sklearn.metrics import accuracy_score, classification_report  # noqa: E402
from sklearn.neural_network import MLPClassifier  # noqa: E402
from sklearn.pipeline import Pipeline  # noqa: E402

from app.config import APP_VERSION, CLASSES, MODEL_PATH  # noqa: E402


def load_fashion_mnist() -> tuple:
    """
    Baixa o Fashion MNIST via tensorflow.keras e prepara os arrays.

    Pré-processamento (deve ser idêntico ao preprocess_image_bytes em model.py):
        - Reshape: (N, 28, 28) → (N, 784)
        - Normalização: uint8 [0, 255] → float32 [0.0, 1.0]
    """
    print("Baixando dataset Fashion MNIST via tensorflow.keras...")
    # Importação tardia para evitar carregar tensorflow na API
    from tensorflow.keras.datasets import fashion_mnist
    (X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()

    # Normalização e Reshape
    X_train = X_train.reshape(-1, 28 * 28).astype("float32") / 255.0
    X_test = X_test.reshape(-1, 28 * 28).astype("float32") / 255.0

    return (X_train, y_train), (X_test, y_test)


def build_pipeline() -> Pipeline:
    """Cria o pipeline sklearn com MLPClassifier."""
    # Hiperparâmetros balanceados para convergência rápida em CPU
    model = MLPClassifier(
        hidden_layer_sizes=(128, 64),
        activation="relu",
        solver="adam",
        max_iter=30,
        random_state=42,
        verbose=True,
    )

    return Pipeline([
        ("model", model),
    ])


def evaluate(pipeline: Pipeline, X_test, y_test) -> dict:
    """Avalia e imprime o relatório de classificação."""
    y_pred = pipeline.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    report = classification_report(
        y_test,
        y_pred,
        target_names=CLASSES,
        output_dict=True,
    )

    print(f"\nAcurácia no teste: {acc:.4f}")
    return {"accuracy": round(float(acc), 4), "report": report}


def save_artifact(pipeline: Pipeline, metrics: dict) -> None:
    """Serializa o modelo e metadados."""
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    artifact = {
        "pipeline": pipeline,
        "algorithm": "MLPClassifier",
        "metrics": metrics,
        "version": APP_VERSION,
        "classes": CLASSES,
    }

    joblib.dump(artifact, MODEL_PATH)
    print(f"\nModelo salvo em: {MODEL_PATH}")


def main() -> None:
    print("=" * 60)
    print("  Fashion MNIST — Treinamento (MLPClassifier)")
    print("=" * 60)

    (X_train, y_train), (X_test, y_test) = load_fashion_mnist()
    print(f"Treino: {len(X_train)} | Teste: {len(X_test)}")

    print("\nIniciando treinamento...")
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    metrics = evaluate(pipeline, X_test, y_test)
    save_artifact(pipeline, metrics)

    print("\nProcesso concluído.")


if __name__ == "__main__":
    main()
