import re
import string


def clean_text(text: str) -> str:
    """
    Normaliza texto SMS para entrada no TfidfVectorizer.

    Passos (ordem importa):
    1. Minúsculas  → reduz o vocabulário ("FREE" == "free")
    2. Remove pontuação → evita tokens como "prize!!!" vs "prize"
    3. Remove espaços extras → vetorização limpa

    Retorna uma string. Nunca levanta exceção para string vazia.
    """
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text
