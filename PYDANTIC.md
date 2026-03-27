# Pydantic v2 — Validação de Dados em APIs

## O que é

Pydantic é a biblioteca de **validação e serialização de dados** usada pelo FastAPI.
Toda vez que uma requisição chega na API, o Pydantic valida o JSON de entrada antes
do seu código ver qualquer dado. Se algo estiver errado, retorna `422 Unprocessable Entity`
automaticamente — sem você escrever nenhum `if`.

---

## Modelo básico

```python
from pydantic import BaseModel

class Produto(BaseModel):
    nome: str
    preco: float
    estoque: int
```

```python
# Válido
p = Produto(nome="Caneta", preco=2.50, estoque=100)
print(p.nome)    # "Caneta"
print(p.preco)   # 2.5

# Inválido → lança ValidationError
p = Produto(nome="Caneta", preco="caro", estoque=100)
# pydantic_core._pydantic_core.ValidationError:
# 1 validation error for Produto
# preco: Input should be a valid number [...]
```

---

## Field — Validações avançadas

`Field` permite adicionar restrições, descrições e exemplos a cada campo.

```python
from pydantic import BaseModel, Field

class DiamondFeatures(BaseModel):
    carat: float = Field(
        ...,              # "..." = campo obrigatório
        ge=0.2,           # greater or equal: carat >= 0.2
        le=5.01,          # less or equal: carat <= 5.01
        description="Peso do diamante em quilates",
        examples=[0.89],
    )
    table: float = Field(..., ge=43.0, le=95.0)
    depth: float = Field(..., ge=43.0, le=79.0)
```

### Referência rápida de restrições numéricas

| Parâmetro | Significado | Exemplo |
|-----------|-------------|---------|
| `ge` | maior ou igual | `ge=0` → não aceita negativos |
| `gt` | estritamente maior | `gt=0` → não aceita zero |
| `le` | menor ou igual | `le=100` → máximo 100 |
| `lt` | estritamente menor | `lt=100` → até 99.99... |

### Restrições de string

```python
from pydantic import Field

nome: str = Field(..., min_length=1, max_length=50)
codigo: str = Field(..., pattern=r"^[A-Z]{3}\d{4}$")
```

---

## Literal — Enum inline

Para campos que só aceitam valores fixos, `Literal` é mais simples que criar um `Enum`:

```python
from typing import Literal

class DiamondFeatures(BaseModel):
    cut: Literal["Fair", "Good", "Very Good", "Premium", "Ideal"]
    color: Literal["D", "E", "F", "G", "H", "I", "J"]
    clarity: Literal["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2", "I1"]
```

```python
# Válido
d = DiamondFeatures(cut="Ideal", color="D", clarity="IF")

# Inválido → 422
d = DiamondFeatures(cut="Perfeito", color="D", clarity="IF")
# Input should be 'Fair', 'Good', 'Very Good', 'Premium' or 'Ideal'
```

---

## ConfigDict — Comportamento do modelo

```python
from pydantic import BaseModel, ConfigDict

class DiamondFeatures(BaseModel):
    model_config = ConfigDict(extra="forbid")  # rejeita campos desconhecidos

    carat: float
    cut: str
```

```python
# Inválido → 422 (campo extra não permitido)
DiamondFeatures(carat=1.0, cut="Ideal", cor="azul")
# Extra inputs are not permitted
```

### Opções de `extra`

| Valor | Comportamento |
|-------|---------------|
| `"forbid"` | Rejeita campos extras com erro 422 |
| `"ignore"` | Aceita mas descarta os campos extras |
| `"allow"` | Aceita e mantém os campos extras |

Para APIs de produção, sempre use `"forbid"` — evita que clientes mandem dados
incorretos sem perceber.

---

## Enum — Valores com semântica

Quando o campo categórico também precisa ser usado como objeto no código:

```python
from enum import Enum
from pydantic import BaseModel

class Island(str, Enum):
    torgersen = "Torgersen"
    biscoe = "Biscoe"
    dream = "Dream"

class PenguinFeatures(BaseModel):
    island: Island
    sex: str
```

```python
p = PenguinFeatures(island="Biscoe", sex="male")
print(p.island)          # Island.biscoe
print(p.island.value)    # "Biscoe"
print(p.island == Island.biscoe)  # True
```

A herança de `str` (`class Island(str, Enum)`) faz o Pydantic aceitar tanto
`"Biscoe"` quanto `Island.biscoe` na entrada.

---

## Modelos de resposta

Pydantic também valida a **saída** da API, não só a entrada:

```python
class PredictionResponse(BaseModel):
    species: str
    confidence: float
    probabilities: dict[str, float]

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str

class ModelInfoResponse(BaseModel):
    version: str
    features: list[str]
    metrics: dict[str, float]
```

No FastAPI, declarar `response_model` garante que a resposta nunca vaze campos
que não deveriam ser expostos:

```python
@app.post("/predict", response_model=PredictionResponse)
def predict(features: DiamondFeatures):
    ...
```

---

## Exemplo completo: exercicio_03

```python
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


CARAT_MIN, CARAT_MAX = 0.2, 5.01
DEPTH_MIN, DEPTH_MAX = 43.0, 79.0
TABLE_MIN, TABLE_MAX = 43.0, 95.0


class DiamondFeatures(BaseModel):
    model_config = ConfigDict(extra="forbid")

    carat:   float = Field(..., ge=CARAT_MIN, le=CARAT_MAX)
    cut:     Literal["Fair", "Good", "Very Good", "Premium", "Ideal"]
    color:   Literal["D", "E", "F", "G", "H", "I", "J"]
    clarity: Literal["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2", "I1"]
    depth:   float = Field(..., ge=DEPTH_MIN, le=DEPTH_MAX)
    table:   float = Field(..., ge=TABLE_MIN, le=TABLE_MAX)
    x:       float = Field(..., ge=0.0, le=10.74)
    y:       float = Field(..., ge=0.0, le=58.9)
    z:       float = Field(..., ge=0.0, le=31.8)


class PriceResponse(BaseModel):
    price_usd: float
    model_version: str
```

### O que acontece em cada caso

```python
# Caso 1: payload válido → 200 OK
DiamondFeatures(carat=0.89, cut="Ideal", color="E", clarity="VS1",
                depth=62.3, table=57.0, x=6.18, y=6.21, z=3.86)

# Caso 2: cut inválido → 422
DiamondFeatures(carat=0.89, cut="Perfeito", ...)
# cut: Input should be 'Fair', 'Good', 'Very Good', 'Premium' or 'Ideal'

# Caso 3: carat fora do range → 422
DiamondFeatures(carat=99.0, cut="Ideal", ...)
# carat: Input should be less than or equal to 5.01

# Caso 4: campo extra → 422
DiamondFeatures(carat=0.89, cut="Ideal", ..., origem="Brasil")
# origem: Extra inputs are not permitted

# Caso 5: campo faltando → 422
DiamondFeatures(carat=0.89, cut="Ideal")
# color: Field required
# clarity: Field required
# ...
```

---

## Convertendo para dict / JSON

```python
features = DiamondFeatures(carat=0.89, cut="Ideal", ...)

# Para dict Python
d = features.model_dump()
# {"carat": 0.89, "cut": "Ideal", ...}

# Para JSON string
j = features.model_json()

# Para DataFrame (usado no predict)
import pandas as pd
df = pd.DataFrame([features.model_dump()])
```

---

## Testando schemas com pytest

```python
import pytest
from pydantic import ValidationError
from app.schemas import DiamondFeatures

VALID = dict(carat=0.89, cut="Ideal", color="E", clarity="VS1",
             depth=62.3, table=57.0, x=6.18, y=6.21, z=3.86)

def test_valid_input():
    d = DiamondFeatures(**VALID)
    assert d.carat == 0.89

def test_invalid_cut_raises():
    with pytest.raises(ValidationError):
        DiamondFeatures(**{**VALID, "cut": "Perfeito"})

def test_carat_out_of_range_raises():
    with pytest.raises(ValidationError):
        DiamondFeatures(**{**VALID, "carat": 99.0})

def test_extra_field_raises():
    with pytest.raises(ValidationError):
        DiamondFeatures(**{**VALID, "campo_extra": "valor"})
```

---

## Resumo

| Recurso | Quando usar |
|---------|-------------|
| `BaseModel` | Sempre — é a base de tudo |
| `Field(ge=, le=)` | Validar ranges numéricos |
| `Field(min_length=, pattern=)` | Validar strings |
| `Literal[...]` | Campos com valores fixos (sem criar Enum) |
| `Enum` | Valores fixos que você também usa como objeto no código |
| `ConfigDict(extra="forbid")` | Rejeitar campos desconhecidos |
| `response_model=` | Garantir que a resposta só exponha o que deve |
