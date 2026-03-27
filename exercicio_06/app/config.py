"""
Configuração centralizada do projeto Fashion MNIST Classifier.
Todas as constantes são definidas aqui e importadas nos outros módulos.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "fashion_classifier.joblib"

APP_VERSION = "1.0.0"
APP_TITLE = "Fashion MNIST Classifier API"
APP_DESCRIPTION = """
## O Curador de Moda

API de classificação de peças de roupa baseada no dataset Fashion MNIST (Zalando).

### Funcionalidades
- **Upload de imagem**: Envie qualquer foto de roupa (JPEG/PNG) e receba a classificação
- **Array de pixels**: Envie diretamente os 784 valores de pixel como JSON

### Pré-processamento automático
A API converte internamente qualquer imagem para o formato que o modelo espera:
`Imagem → Escala de cinza → 28×28 pixels → Array normalizado [0, 1]`
"""

IMAGE_SIZE = 28
N_PIXELS = IMAGE_SIZE * IMAGE_SIZE  # 784

CLASSES = [
    "Camiseta/Top",  # 0
    "Calça",         # 1
    "Pullover",      # 2
    "Vestido",       # 3
    "Casaco",        # 4
    "Sandália",      # 5
    "Camisa",        # 6
    "Tênis",         # 7
    "Bolsa",         # 8
    "Bota",          # 9
]

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/bmp",
}
