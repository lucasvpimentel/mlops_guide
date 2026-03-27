# Guia de Comandos: GitHub Actions & Flake8 (Linter)

Este documento contém os comandos, definições e configurações essenciais para automatizar a qualidade do seu código.

---

## 🧹 Flake8 (O Linter)

### O que é?
O **Flake8** é uma ferramenta de "Linting" para Python. Ele é, na verdade, uma combinação de três ferramentas populares (`PyFlakes`, `pycodestyle` e `McCabe`). O seu objetivo é analisar o código-fonte em busca de erros de programação, bugs, erros de estilo e construções suspeitas, garantindo que o seu projeto siga as normas da **PEP 8** (o manual de estilo oficial do Python).

### Comandos de Terminal

| Comando | Descrição |
|---------|-----------|
| `pip install flake8` | Instala o linter no seu ambiente. |
| `flake8 .` | Analisa todos os arquivos da pasta atual e subpastas. |
| `flake8 arquivo.py` | Analisa um arquivo específico. |
| `flake8 --count --statistics` | Mostra o número total de erros e estatísticas. |

---

## 🤖 YAML / YML (A Linguagem de Configuração)

### O que é?
**YAML** (abreviação de *YAML Ain't Markup Language*) é uma linguagem de serialização de dados legível por humanos. Ela é amplamente utilizada para arquivos de configuração, como os do GitHub Actions, Docker Compose e Kubernetes. 

### Diferença entre .yaml e .yml?
Nenhuma! Ambas as extensões são válidas e referem-se à mesma linguagem. O uso de **.yml** tornou-se popular em sistemas mais antigos que suportavam apenas extensões de três letras (como no Windows antigo), enquanto **.yaml** é a extensão oficial. No GitHub Actions, você pode usar qualquer uma delas, mas o padrão da comunidade costuma ser **.yml**.

### Regras de Ouro do YAML
1. **Indentação:** É baseada em espaços (nunca use a tecla TAB).
2. **Key: Value:** O formato básico é sempre uma chave seguida de dois pontos e um espaço (ex: `name: Meu Robô`).
3. **Listas:** Itens de uma lista começam com um hífen e um espaço (ex: `- run: echo "Olá"`).

---

## 🚀 GitHub Actions (Automação)

### Estrutura do Arquivo YAML (.yml)

```yaml
name: Nome do Workflow    # Nome que aparece na aba Actions

on: [push]                # EVENTO: O que dispara o robô (push, pull_request)

jobs:                     # TRABALHOS: O que o robô vai fazer
  lint:                   # Nome do job (pode ser qualquer um)
    runs-on: ubuntu-latest # SISTEMA: Onde o robô vai rodar (Linux, Windows)
    steps:                # PASSOS: A lista de tarefas
      - uses: actions/checkout@v4       # 1. Baixa seu código no robô
      - uses: actions/setup-python@v5    # 2. Instala o Python no robô
      - run: pip install flake8         # 3. Instala o linter
      - run: flake8 .                   # 4. Roda a verificação
```

### Palavras-Chave Principais

- **`on`**: Define o gatilho (Trigger).
- **`uses`**: Chama uma ação pronta (um "plugin") do GitHub.
- **`run`**: Executa um comando de terminal direto no sistema do robô.
- **`needs`**: Faz um job esperar outro acabar (sequenciamento).

---

## 💡 Dicas de Boas Práticas

1. **Arquivo `.flake8`:** Em vez de comandos longos, use um arquivo de configuração na raiz:
    ```ini
    [flake8]
    ignore = E501
    max-line-length = 127
    exclude = .venv, __pycache__
    ```
2. **Fail Fast:** O Linter deve ser o primeiro passo. Se o código não estiver no padrão, o processo para imediatamente.
