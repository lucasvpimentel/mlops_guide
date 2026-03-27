from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "modelo_energia.joblib"

# API Metadata
APP_VERSION = "1.0.0"
APP_TITLE = "Energy Efficiency API"
APP_DESCRIPTION = (
    "Predição de Heating Load (carga de aquecimento) para edifícios "
    "com base no dataset UCI Energy Efficiency."
)

# Regras de Validação Física (Constraints do Dataset UCI)
# X1: Relative Compactness
RC_MIN, RC_MAX = 0.62, 0.98
# X2: Surface Area
SA_MIN, SA_MAX = 514.5, 808.5
# X3: Wall Area
WA_MIN, WA_MAX = 245.0, 416.5
# X4: Roof Area
RA_MIN, RA_MAX = 110.25, 220.5
# X5: Overall Height
OH_MIN, OH_MAX = 3.5, 7.0
# X6: Orientation (2:North, 3:East, 4:South, 5:West)
VALID_ORIENTATIONS = [2, 3, 4, 5]
# X7: Glazing Area (0%, 10%, 25%, 40%)
GA_MIN, GA_MAX = 0.0, 0.4
# X8: Glazing Area Distribution
VALID_GLAZING_DIST = [0, 1, 2, 3, 4, 5]
