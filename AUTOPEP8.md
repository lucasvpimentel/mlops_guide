# autopep8 — Formatação Automática de Código Python

---

## O que é PEP 8

**PEP** significa *Python Enhancement Proposal* — são documentos oficiais que propõem
melhorias para a linguagem Python. O **PEP 8** especificamente é o guia de estilo
oficial para código Python, publicado em 2001 por Guido van Rossum (criador do Python).

O objetivo do PEP 8 não é tornar o código "bonito", mas sim **legível e consistente**:
qualquer desenvolvedor Python deve conseguir ler o código de outra pessoa sem estranheza.

### As regras mais importantes do PEP 8

**Indentação e espaçamento:**
```python
# Correto: 4 espaços por nível
def soma(a, b):
    return a + b

# Errado: tab ou 2 espaços
def soma(a, b):
  return a + b
```

**Comprimento de linha:**
```python
# PEP 8 original: máximo 79 caracteres
# Projetos modernos costumam usar 99 ou 100 (configurável no .flake8)

# Correto: linha dentro do limite
resultado = soma(valor_a, valor_b)

# Errado: linha muito longa
resultado = minha_funcao_com_nome_longo(parametro_um=valor_um, parametro_dois=valor_dois, parametro_tres=valor_tres)
```

**Linhas em branco:**
```python
# Correto: 2 linhas em branco entre funções/classes no nível do módulo
def funcao_a():
    pass


def funcao_b():
    pass


class MinhaClasse:

    def metodo_a(self):       # 1 linha em branco entre métodos
        pass

    def metodo_b(self):
        pass
```

**Imports:**
```python
# Correto: um import por linha, agrupados (stdlib → third-party → local)
import os
import sys

import pandas as pd
import numpy as np

from app.config import MODEL_PATH

# Errado: múltiplos imports na mesma linha
import os, sys
```

**Espaços em operadores e comentários:**
```python
# Correto
x = 1
y = x + 2
z = [1, 2, 3]
resultado = funcao(a=1, b=2)
x = 1  # dois espaços antes do comentário inline

# Errado
x=1
y = x+2
z = [ 1, 2, 3 ]
resultado = funcao( a = 1, b = 2 )
x = 1 # um espaço só
```

**Nomes:**
```python
# Variáveis e funções: snake_case
minha_variavel = 10
def calcular_preco():
    pass

# Classes: PascalCase
class DiamondPredictor:
    pass

# Constantes: UPPER_SNAKE_CASE
MODEL_PATH = "model/diamond.joblib"
MAX_RETRIES = 3
```

### Códigos de erro do flake8

O `flake8` usa códigos para identificar cada tipo de violação:

| Prefixo | Categoria | Exemplos |
|---------|-----------|---------|
| `E1xx` | Indentação | `E101` tab/espaço misturado |
| `E2xx` | Espaços em branco | `E201` espaço após `[`, `E261` comentário inline |
| `E3xx` | Linhas em branco | `E302` falta 2 linhas antes de classe |
| `E4xx` | Imports | `E401` múltiplos imports na linha |
| `E5xx` | Comprimento de linha | `E501` linha muito longa |
| `E7xx` | Declarações | `E711` comparação com `None` |
| `W` | Avisos | `W291` espaço no final da linha |
| `F` | Erros lógicos (pyflakes) | `F401` import não usado, `F821` nome indefinido |

> Códigos `E` e `W` são puramente de estilo. Códigos `F` indicam problemas reais
> no código — como um import que não serve para nada ou uma variável usada antes
> de ser definida.

---

## O que é autopep8

`autopep8` é uma ferramenta que **corrige automaticamente** violações de estilo PEP 8
no seu código Python. Em vez de corrigir manualmente cada aviso do `flake8`, você
roda o autopep8 e ele ajusta o arquivo por você.

```
flake8   →  aponta os problemas
autopep8 →  corrige os problemas
```

---

## Instalação

```bash
pip install autopep8
```

---

## Uso básico

### Ver o que seria corrigido (sem alterar o arquivo)

```bash
autopep8 app/main.py
```

Imprime o arquivo corrigido no terminal. Nada é salvo.

### Corrigir um arquivo (sobrescreve)

```bash
autopep8 --in-place app/main.py
```

### Corrigir todos os arquivos de uma pasta

```bash
autopep8 --in-place --recursive app/
autopep8 --in-place --recursive train/
autopep8 --in-place --recursive tests/
```

---

## Exemplos de correções automáticas

### Espaçamento em comentários (E261, E262)

```python
# Antes
x = 1 # meu comentário

# Depois
x = 1  # meu comentário
```

### Linha em branco faltante antes de classe (E302)

```python
# Antes
CONSTANTE = 42
class MinhaClasse:
    pass

# Depois
CONSTANTE = 42


class MinhaClasse:
    pass
```

### Linha muito longa (E501)

```python
# Antes
pipeline = Pipeline([("scaler", StandardScaler()), ("clf", RandomForestClassifier(n_estimators=100, random_state=42))])

# Depois (quebra automática)
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", RandomForestClassifier(
        n_estimators=100, random_state=42))
])
```

### Espaços em excesso (E201, E202, E203)

```python
# Antes
x = [ 1, 2, 3 ]
y = dict ['key']

# Depois
x = [1, 2, 3]
y = dict['key']
```

### Imports duplicados / espaçamento (E401)

```python
# Antes
import os, sys

# Depois
import os
import sys
```

---

## Configurando o limite de linha

Por padrão o autopep8 usa 79 caracteres (PEP 8 original).
Para alinhar com o `.flake8` deste repositório (100 caracteres):

```bash
autopep8 --in-place --max-line-length 100 app/main.py
```

Ou crie um `setup.cfg` na raiz:

```ini
[pycodestyle]
max-line-length = 100
```

Com isso, `autopep8` e `flake8` usam o mesmo limite automaticamente.

---

## O que autopep8 NÃO corrige

Algumas violações exigem decisão humana e o autopep8 ignora:

| Código | Problema | Por quê não corrige |
|--------|----------|---------------------|
| F401 | Import não utilizado | Não sabe se foi intencional |
| F811 | Redefinição de nome | Pode ser lógica intencional |
| E402 | Import fora do topo | Pode ser necessário (ex: `sys.path`) |
| E711 | `== None` em vez de `is None` | Mudança semântica |

Para esses casos, a correção é manual.

---

## Fluxo recomendado antes do push

```bash
# 1. Formatar automaticamente
autopep8 --in-place --recursive --max-line-length 100 app/ train/ tests/

# 2. Verificar o que ainda resta
flake8 app/ train/ tests/

# 3. Corrigir manualmente o que sobrar (F401, E402, etc.)

# 4. Rodar os testes
pytest tests/ -v
```

---

## Diferença entre autopep8, black e isort

| Ferramenta | O que faz | Estilo |
|------------|-----------|--------|
| `autopep8` | Corrige violações PEP 8 | Conservador — mínima mudança |
| `black` | Reformata tudo | Opinionado — força um estilo único |
| `isort` | Ordena imports | Agrupa e ordena `import` e `from` |

Para projetos educacionais como este, `autopep8` é o mais simples de adotar
porque só toca o que está errado, sem reformatar o código inteiro.
