"""
Configuração centralizada do projeto Diamond Price Predictor.

Todas as constantes do projeto são definidas aqui e importadas nos outros módulos.
Isso evita "números mágicos" espalhados pelo código e facilita manutenção.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Caminhos de arquivo
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "diamond_price_model.joblib"

# ---------------------------------------------------------------------------
# Metadados da API
# ---------------------------------------------------------------------------
APP_VERSION = "1.0.0"
APP_TITLE = "Diamond Price Predictor API"
APP_DESCRIPTION = """
## 💎 Diamond Price Predictor

API de estimativa de preço de diamantes baseada no dataset clássico `diamonds` (ggplot2).

### Funcionalidades
- **Predição de preço**: Envie as características do diamante e receba a estimativa em USD
- **Conteinerização total**: Rode via Docker sem instalar Python localmente

### Features utilizadas
| Feature | Tipo | Descrição |
|---------|------|-----------|
| carat | float | Peso do diamante em quilates |
| cut | string | Qualidade do corte |
| color | string | Cor (D = melhor → J = pior) |
| clarity | string | Clareza (IF = melhor → I1 = pior) |
| depth | float | Profundidade total (%) |
| table | float | Largura do topo relativa ao ponto mais largo (%) |
| x | float | Comprimento em mm |
| y | float | Largura em mm |
| z | float | Profundidade em mm |
"""

# ---------------------------------------------------------------------------
# Valores válidos para variáveis categóricas (domínio do dataset)
# ---------------------------------------------------------------------------
VALID_CUTS = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
VALID_COLORS = ["D", "E", "F", "G", "H", "I", "J"]
VALID_CLARITIES = ["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2", "I1"]

# ---------------------------------------------------------------------------
# Limites físicos das features numéricas (derivados do dataset real)
# ---------------------------------------------------------------------------
CARAT_MIN, CARAT_MAX = 0.2, 5.01
DEPTH_MIN, DEPTH_MAX = 43.0, 79.0
TABLE_MIN, TABLE_MAX = 43.0, 95.0
X_MIN, X_MAX = 0.0, 10.74
Y_MIN, Y_MAX = 0.0, 58.9
Z_MIN, Z_MAX = 0.0, 31.8
