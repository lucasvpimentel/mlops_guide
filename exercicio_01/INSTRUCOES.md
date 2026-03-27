# Instruções — Identificador de Pinguins

Guia completo para replicar o projeto do zero: ambiente, treinamento, API e testes.

---

## Pré-requisitos

- Python 3.9 ou superior instalado
- `pip` disponível no terminal
- Acesso à internet (para instalar dependências e baixar o dataset)

Verifique sua versão:

```bash
python --version
pip --version
```

---

## Estrutura do projeto

```
exercicio_01/
├── app/
│   ├── __init__.py
│   ├── main.py          # Aplicação FastAPI
│   ├── schemas.py       # Contratos Pydantic (entrada/saída)
│   ├── model.py         # Carregamento e predição
│   └── config.py        # Constantes e configurações
├── model/
│   └── penguin_classifier.joblib   # Gerado pelo script de treino
├── train/
│   └── train_model.py   # Script de treinamento
├── tests/
│   ├── test_schemas.py  # Testes unitários de validação
│   └── test_api.py      # Testes de integração da API
├── requirements.txt
├── Dockerfile           # Opcional — containerização
├── TEORIA.md
└── INSTRUCOES.md
```

---

## Passo 1 — Criar e ativar o ambiente virtual

Um ambiente virtual isola as dependências do projeto do Python global do sistema.

**Linux / macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

Você verá `(.venv)` no início do prompt quando o ambiente estiver ativo.

---

## Passo 2 — Instalar as dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

As principais bibliotecas instaladas:

| Biblioteca | Finalidade |
|-----------|-----------|
| `fastapi` | Framework da API REST |
| `uvicorn` | Servidor ASGI para rodar o FastAPI |
| `pydantic` | Validação de dados e contratos |
| `scikit-learn` | Treinamento do modelo de classificação |
| `pandas` | Manipulação do dataset |
| `seaborn` | Download do dataset Palmer Penguins |
| `joblib` | Serialização do modelo |
| `pytest` + `httpx` | Testes automatizados |

---

## Passo 3 — Treinar o modelo

O script baixa o dataset, treina um Random Forest e salva o modelo em `model/`.

```bash
python train/train_model.py
```

Saída esperada:

```
Carregando dataset Palmer Penguins via seaborn...
  Registros brutos: 344
  Registros após remover nulos: 333
  Treino: 266 | Teste: 67
Treinando RandomForestClassifier...

Acurácia no conjunto de teste: 0.9851 (98.5%)

Relatório de classificação:
              precision    recall  f1-score   support
      Adelie       0.98      1.00      0.99        44
   Chinstrap       1.00      0.94      0.97        16
      Gentoo       1.00      1.00      1.00        27
    accuracy                           0.99        87
   macro avg       0.99      0.98      0.99        87

Modelo salvo em: .../model/penguin_classifier.joblib
Treinamento concluído com sucesso.
```

Verifique que o arquivo foi gerado:

```bash
# Linux/macOS
ls model/

# Windows
dir model\
```

---

## Passo 4 — Subir a API

```bash
uvicorn app.main:app --reload
```

A flag `--reload` reinicia automaticamente a API quando você salvar alterações no código (útil para desenvolvimento).

Saída esperada:

```
INFO:     Iniciando API — carregando modelo...
INFO:     Modelo carregado com sucesso de '.../model/penguin_classifier.joblib'.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## Passo 5 — Explorar a API

### Documentação interativa (Swagger UI)

Abra no navegador: [http://localhost:8000/docs](http://localhost:8000/docs)

Você verá todos os endpoints documentados. Clique em **POST /predict → Try it out** para testar direto no browser.

### Endpoints disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/health` | Status da API e do modelo |
| `GET` | `/info` | Metadados do modelo |
| `POST` | `/predict` | Classificar um pinguim |

---

## Passo 6 — Fazer uma predição (exemplos)

### Via curl (terminal)

**Predição válida — pinguim Adelie típico:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "bill_length_mm": 39.1,
    "bill_depth_mm": 18.7,
    "flipper_length_mm": 181.0,
    "body_mass_g": 3750.0,
    "island": "Torgersen",
    "sex": "male"
  }'
```

**Resposta esperada:**
```json
{
  "species": "Adelie",
  "confidence": 0.97,
  "probabilities": {
    "Adelie": 0.97,
    "Chinstrap": 0.02,
    "Gentoo": 0.01
  }
}
```

**Predição inválida — peso negativo (deve retornar 422):**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "bill_length_mm": 39.1,
    "bill_depth_mm": 18.7,
    "flipper_length_mm": 181.0,
    "body_mass_g": -500,
    "island": "Torgersen",
    "sex": "male"
  }'
```

**Resposta esperada (HTTP 422):**
```json
{
  "detail": [
    {
      "type": "greater_than_equal",
      "loc": ["body", "body_mass_g"],
      "msg": "Input should be greater than or equal to 500",
      "input": -500.0
    }
  ]
}
```

### Via Python

```python
import httpx

payload = {
    "bill_length_mm": 47.5,
    "bill_depth_mm": 14.2,
    "flipper_length_mm": 209.0,
    "body_mass_g": 5200.0,
    "island": "Biscoe",
    "sex": "female",
}

response = httpx.post("http://localhost:8000/predict", json=payload)
print(response.json())
```

---

## Passo 7 — Executar os testes

### Testes unitários (não requerem a API no ar)

```bash
pytest tests/test_schemas.py -v
```

### Testes de integração (requerem o modelo treinado)

```bash
pytest tests/test_api.py -v
```

### Todos os testes

```bash
pytest -v
```

Saída esperada: todos os testes passando (`PASSED`).

---

## Passo 8 — (Opcional) Docker

> Este passo é apenas ilustrativo. A forma principal de execução é via `.venv` (passos acima).

**Pré-requisito:** Docker instalado e rodando.

**Importante:** o modelo deve ser treinado localmente **antes** do build, pois o Dockerfile copia o arquivo `model/` para dentro da imagem.

```bash
# 1. Garantir que o modelo foi treinado
python train/train_model.py

# 2. Build da imagem
docker build -t penguin-classifier .

# 3. Rodar o container
docker run -p 8000:8000 penguin-classifier
```

A API estará disponível em [http://localhost:8000/docs](http://localhost:8000/docs), exatamente como no passo 4.

**Por que isso é relevante em MLOps?**
O container empacota o código, as dependências e o modelo em uma unidade imutável e portável. O mesmo container que roda na sua máquina roda em qualquer servidor de produção — eliminando o clássico problema "funciona na minha máquina".

---

## Regras de validação (referência rápida)

| Campo | Tipo | Valores aceitos |
|-------|------|----------------|
| `bill_length_mm` | float | 10.0 a 80.0 mm |
| `bill_depth_mm` | float | 5.0 a 30.0 mm |
| `flipper_length_mm` | float | 100.0 a 300.0 mm |
| `body_mass_g` | float | 500.0 a 10.000 g (nunca negativo) |
| `island` | string | `"Torgersen"`, `"Biscoe"`, `"Dream"` |
| `sex` | string | `"male"`, `"female"` |

Qualquer valor fora dessas regras retorna **HTTP 422** com uma mensagem indicando exatamente qual campo está inválido.

---

## Solução de problemas

**`FileNotFoundError: Modelo não encontrado`**
→ Execute `python train/train_model.py` antes de subir a API.

**`ModuleNotFoundError: No module named 'app'`**
→ Certifique-se de rodar os comandos a partir da raiz do projeto (`exercicio_01/`), não de dentro de uma subpasta.

**`422 Unprocessable Entity` inesperado**
→ Verifique se todos os campos estão presentes e dentro dos limites da tabela acima.

**Porta 8000 já em uso**
→ Rode em outra porta: `uvicorn app.main:app --reload --port 8001`
