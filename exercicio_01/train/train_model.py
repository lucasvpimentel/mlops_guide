"""
Script de treinamento do classificador de espécies de pinguins.

O script carrega os dados brutos, realiza o pré-processamento das
variáveis, treina um classificador RandomForest, avalia o desempenho
e salva o artefato do modelo final.

Execução:
    python train/train_model.py

Saída:
    model/penguin_classifier.joblib (Pipeline treinado e metadados)
"""

import sys
from pathlib import Path

# Garante que o módulo app seja encontrado ao rodar da raiz do projeto
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402
from sklearn.ensemble import RandomForestClassifier  # noqa: E402
from sklearn.metrics import (  # noqa: E402
    classification_report,
    accuracy_score,
)
from sklearn.model_selection import train_test_split  # noqa: E402
from sklearn.pipeline import Pipeline  # noqa: E402
from sklearn.preprocessing import LabelEncoder, StandardScaler  # noqa: E402

from app.config import MODEL_PATH, SPECIES  # noqa: E402

# Definição das colunas usadas para entrada (features) e do alvo da
# predição (target)
FEATURE_COLUMNS = [
    "bill_length_mm",
    "bill_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
    "island",
    "sex",
]
TARGET_COLUMN = "species"
# Seed para garantir reprodutibilidade nos experimentos
RANDOM_STATE = 42


def load_and_prepare_data() -> tuple[pd.DataFrame, pd.Series]:
    """
    Carrega o dataset Palmer Penguins e realiza limpeza e codificação básica.
    """
    print("Carregando dataset Palmer Penguins via seaborn...")
    df = sns.load_dataset("penguins")

    print(f"  Registros brutos: {len(df)}")
    # Remove linhas que possuem valores nulos nas colunas de interesse
    # (limpeza de dados)
    df = df.dropna(subset=FEATURE_COLUMNS + [TARGET_COLUMN])
    print(f"  Registros após remover nulos: {len(df)}")

    # Codificação de variáveis categóricas para formato numérico legível
    # pelo scikit-learn
    # LabelEncoder transforma classes textuais em números inteiros
    # (ex: male -> 0, female -> 1)
    df["island"] = LabelEncoder().fit_transform(df["island"])
    df["sex"] = LabelEncoder().fit_transform(df["sex"])

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    return X, y


def train(X_train: pd.DataFrame, y_train: pd.Series) -> Pipeline:
    """
    Cria e treina um pipeline de machine learning.
    O pipeline inclui a normalização das features e o classificador final.
    """
    print("Treinando RandomForestClassifier...")
    # Usamos um Pipeline para encapsular o escalonamento e o modelo em um
    # único objeto
    pipeline = Pipeline([
        ("scaler", StandardScaler()),  # Normaliza os dados
        ("clf", RandomForestClassifier(
            n_estimators=100,           # Quantidade de árvores na floresta
            random_state=RANDOM_STATE,  # Fixa a aleatoriedade
            class_weight="balanced",    # Trata classes desbalanceadas
        )),
    ])
    pipeline.fit(X_train, y_train)
    return pipeline


def evaluate(
    pipeline: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> None:
    """
    Avalia a performance do modelo no conjunto de dados de teste.
    """
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nAcurácia no conjunto de teste: {acc:.4f} ({acc*100:.1f}%)")
    print("\nRelatório de classificação:")
    # Exibe métricas detalhadas (precision, recall, f1-score) para cada classe
    print(
        classification_report(y_test, y_pred, target_names=sorted(SPECIES))
    )


def save_model(pipeline: Pipeline) -> None:
    """
    Salva o pipeline e os metadados necessários em um arquivo .joblib.
    """
    # Cria o diretório de destino caso ele não exista
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Salva o pipeline junto com metadados para que a API use as features
    # corretas
    artifact = {
        "pipeline": pipeline,
        "feature_names": FEATURE_COLUMNS,
        "class_names": sorted(SPECIES),
    }
    joblib.dump(artifact, MODEL_PATH)
    print(f"\nModelo salvo em: {MODEL_PATH}")


def main() -> None:
    """
    Fluxo principal: carregamento, divisão, treino, avaliação e salvamento.
    """
    X, y = load_and_prepare_data()

    # Divide os dados entre Treino (80%) e Teste (20%)
    # Stratify mantém a proporção de cada espécie em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    print(f"  Treino: {len(X_train)} | Teste: {len(X_test)}")

    # Executa as etapas de modelagem
    pipeline = train(X_train, y_train)
    evaluate(pipeline, X_test, y_test)
    save_model(pipeline)
    print("\nTreinamento concluído com sucesso.")


if __name__ == "__main__":
    main()
