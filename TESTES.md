# 🧪 Guia de Testes Unitários: Pytest & Pydantic em IA

Testar o código é tão importante quanto validar o modelo.

---

## 1. Pytest 🚀

O **Pytest** é a ferramenta padrão para escrever e rodar testes em Python de forma simples.

```python
def test_clean_text_basic():
    entrada = "  OLÁ MUNDO!  "
    esperado = "olá mundo!"
    assert entrada.strip().lower() == esperado
```

---

## 2. Pydantic 🛡️

O **Pydantic** define o **Contrato** da sua API.

```python
from pydantic import BaseModel, Field

class DiamondInput(BaseModel):
    carat: float = Field(..., gt=0)
    cut: str
```
