# Como Testar Localmente Antes do Push

Este guia replica exatamente o que o GitHub Actions executa em cada pipeline de CI.
Se todos os passos abaixo passarem na sua máquina, o push não vai quebrar.

---

## Pré-requisitos

- Python 3.11+
- `pip` atualizado
- Docker instalado (apenas para os exercícios que fazem build de imagem)

---

## Regra geral

Cada exercício tem seu próprio ambiente isolado. O padrão é sempre:

```
cd exercicio_XX/
python -m venv .venv
source .venv/Scripts/activate   # Windows (bash)
# ou: source .venv/bin/activate  # Linux/macOS
pip install --upgrade pip
pip install flake8
pip install -r requirements.txt
```

Depois disso, os comandos específicos de cada exercício.

---

## Exercício 01 — Classificador de Pinguins

```bash
cd exercicio_01/
export PYTHONPATH=$(pwd)          # Linux/macOS
# ou: set PYTHONPATH=%CD%         # Windows CMD
# ou: $env:PYTHONPATH = (pwd)     # Windows PowerShell

flake8 app/ train/ tests/
python train/train_model.py
pytest tests/ -v
docker build -t exercicio_01 .
```

**Testes incluídos:** `test_schemas.py` + `test_api.py`
**Requer modelo treinado antes de rodar pytest:** sim

---

## Exercício 02 — Previsão de Gorjetas

```bash
cd exercicio_02/
export PYTHONPATH=$(pwd)

flake8 app/ train/ tests/
python train/train.py
pytest tests/ -v
docker build -t exercicio_02 .
```

**Testes incluídos:** `test_schemas.py` + `test_api.py`
**Requer modelo treinado antes de rodar pytest:** sim

---

## Exercício 03 — Preço de Diamantes

```bash
cd exercicio_03/
export PYTHONPATH=$(pwd)

flake8 app/ train/ tests/
python train/train.py
pytest tests/ -v
docker build -t exercicio_03 .
```

**Testes incluídos:** `test_schemas.py` + `test_api.py`
**Requer modelo treinado antes de rodar pytest:** sim

---

## Exercício 04 — Diagnóstico Cardíaco

```bash
cd exercicio_04/
export PYTHONPATH=$(pwd)

flake8 app/ train/ tests/
python train/train.py
pytest tests/ -v
```

> Sem Docker neste exercício.

**Testes incluídos:** `test_schemas.py` + `test_api.py`
**Requer modelo treinado antes de rodar pytest:** sim

---

## Exercício 05 — Avaliação de Carros

```bash
cd exercicio_05/
export PYTHONPATH=$(pwd)

flake8 app/ src/
```

> Sem testes automatizados e sem Docker neste exercício — o CI só executa o linter.

---

## Exercício 06 — Curador de Moda (Fashion MNIST)

```bash
cd exercicio_06/
export PYTHONPATH=$(pwd)

pip install -r requirements.txt --ignore-requires-python
flake8 app/ train/ tests/
pytest tests/test_schemas.py -v
```

> O treino (`python train/train.py`) **não é executado no CI** porque depende de
> TensorFlow e leva vários minutos. Rode localmente se quiser testar o modelo completo.
> Os testes de integração (`test_api.py`) também exigem o modelo treinado e ficam
> fora do CI por esse motivo.

**Testes incluídos no CI:** apenas `test_schemas.py` (sem dependência de modelo)
**Para rodar tudo localmente (opcional):**

```bash
python train/train.py          # ~5 min, baixa ~30MB do Fashion MNIST
pytest tests/ -v               # inclui test_api.py
```

---

## Exercício 07 — Detecção de Spam

```bash
cd exercicio_07/
export PYTHONPATH=$(pwd)

flake8 app/ src/ tests/
python src/train.py
pytest tests/ -v
docker build -t exercicio_07 .
```

**Testes incluídos:** `test_preprocess.py`
**Requer modelo treinado antes de rodar pytest:** sim

---

## Verificando o linter para todos de uma vez

Para checar flake8 em todos os exercícios sem precisar entrar em cada pasta:

```bash
# Da raiz do repositório
for ex in exercicio_0{1,2,3,4,5,6,7}; do
  echo "=== $ex ==="
  (cd $ex && python -m flake8 app/ train/ tests/ src/ 2>/dev/null || true)
done
```

> O `.flake8` na raiz define `max-line-length = 100` para todos.

---

## Resumo por exercício

| Exercício | Linter | Treino | Pytest | Docker |
|-----------|--------|--------|--------|--------|
| 01 — Pinguins | `app/ train/ tests/` | `train/train_model.py` | `tests/` | sim |
| 02 — Gorjetas | `app/ train/ tests/` | `train/train.py` | `tests/` | sim |
| 03 — Diamantes | `app/ train/ tests/` | `train/train.py` | `tests/` | sim |
| 04 — Coração | `app/ train/ tests/` | `train/train.py` | `tests/` | não |
| 05 — Carros | `app/ src/` | — | — | não |
| 06 — Moda | `app/ train/ tests/` | — (pesado) | `tests/test_schemas.py` | não |
| 07 — Spam | `app/ src/ tests/` | `src/train.py` | `tests/` | sim |

---

## Dica: script de verificação rápida

Salve como `check.sh` na raiz e rode `bash check.sh EX` onde `EX` é o número do exercício:

```bash
#!/usr/bin/env bash
# Uso: bash check.sh 01
EX="exercicio_0$1"
echo "Verificando $EX..."
cd "$EX" || exit 1
export PYTHONPATH=$(pwd)
python -m flake8 app/ train/ tests/ src/ 2>/dev/null
echo "Lint OK"
```
