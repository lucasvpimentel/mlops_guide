from pathlib import Path

# Definição de caminhos (Paths) do projeto
# BASE_DIR aponta para a raiz da pasta exercicio_01
BASE_DIR = Path(__file__).resolve().parent.parent
# Caminho completo para o arquivo do modelo treinado (.joblib)
MODEL_PATH = BASE_DIR / "model" / "penguin_classifier.joblib"

# Metadados básicos da API para exibição na documentação automática (Swagger/Redoc)
APP_VERSION = "1.0.0"
APP_TITLE = "Penguin Species Classifier"
APP_DESCRIPTION = (
    "API para classificação de espécies de pinguins do dataset Palmer Penguins. "
    "Prediz Adelie, Chinstrap ou Gentoo com base em medidas físicas."
)

# Limites físicos das features (Domain Knowledge)
# Esses valores são usados para validação de dados de entrada na API (Pydantic)
# para garantir que os valores enviados façam sentido biologicamente.

BILL_LENGTH_MIN = 10.0
BILL_LENGTH_MAX = 80.0

BILL_DEPTH_MIN = 5.0
BILL_DEPTH_MAX = 30.0

FLIPPER_LENGTH_MIN = 100.0
FLIPPER_LENGTH_MAX = 300.0

BODY_MASS_MIN = 500.0
BODY_MASS_MAX = 10_000.0

# Lista oficial das espécies (classes) que o modelo é capaz de predizer
SPECIES = ["Adelie", "Chinstrap", "Gentoo"]
