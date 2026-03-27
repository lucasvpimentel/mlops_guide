import pathlib

import joblib
from datasets import load_dataset
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

from src.preprocessing import clean_text

# Caminhos relativos à raiz do projeto
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model.joblib"


def load_data_hf() -> pd.DataFrame:
    """Baixa o dataset sms_spam do Hugging Face e padroniza para o pipeline.

    O HF entrega:
      - coluna 'sms'   → renomeada para 'text'
      - coluna 'label' → inteiros 0 (ham) e 1 (spam), sem mapeamento adicional
    """
    ds = load_dataset("sms_spam", split="train")
    df = ds.to_pandas()
    df = df.rename(columns={"sms": "text"})
    return df


def build_pipeline() -> Pipeline:
    """
    Pipeline sklearn: vetorização TF-IDF → classificador Naive Bayes.

    TfidfVectorizer: converte texto limpo em matriz de frequência ponderada.
    MultinomialNB: modelo probabilístico eficiente para texto esparso.
    """
    return Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", MultinomialNB()),
    ])


def train_and_save() -> None:
    print("[train] Baixando dataset via Hugging Face (sms_spam)...")
    df = load_data_hf()

    # Aplicar a mesma função de limpeza que será usada na inferência
    df["text"] = df["text"].apply(clean_text)

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"],
        test_size=0.2,
        random_state=42,
        stratify=df["label"],
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"[train] Acurácia no conjunto de teste: {acc:.4f}")
    print(classification_report(y_test, y_pred, target_names=["ham", "spam"]))

    joblib.dump(pipeline, MODEL_PATH)
    print(f"[train] Modelo salvo em: {MODEL_PATH}")


if __name__ == "__main__":
    train_and_save()
