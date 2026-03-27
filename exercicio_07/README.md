# Spam Detection API — MLOps Project

Sistema de detecção de SMS spam que demonstra a jornada de um modelo de Machine Learning do ambiente de pesquisa até a produção, com testes automatizados, empacotamento Docker e pipeline CI/CD.

Para entender os conceitos por trás deste projeto, veja o [Guia de Teoria Aplicada](TEORIA.md) e o [Guia de GitHub Actions](GITHUB_ACTIONS.md).

---

## 🏗️ Estrutura do Projeto

```
exercicio_01/
├── .github/workflows/
│   └── main.yml           # Pipeline CI/CD (GitHub Actions)
├── app/
│   ├── __init__.py
│   ├── main.py            # Servidor FastAPI — endpoints HTTP
│   └── model_loader.py    # Carregamento do modelo e inferência
├── src/
│   ├── __init__.py
│   ├── preprocessing.py   # Limpeza de texto (função testável)
│   └── train.py           # Script de treinamento
├── tests/
│   ├── __init__.py
│   └── test_preprocess.py # Testes unitários (pytest)
├── data/
│   └── SMSSpamCollection  # Dataset UCI SMS Spam
├── .dockerignore
├── .gitignore
├── Dockerfile
├── model.joblib           # Artefato gerado pelo train.py
└── requirements.txt
```

---

## 🧠 Como o Código Funciona

O projeto segue uma arquitetura modular que separa as fases de **treinamento**, **testes** e **serviço**.

1.  **Pré-processamento (`src/preprocessing.py`):**
    *   Toda mensagem (no treino e na API) passa pela mesma função `clean_text`.
    *   Ela normaliza o texto (minúsculas, remoção de pontuação e espaços extras) para garantir que o modelo receba dados limpos e consistentes.

2.  **Treinamento (`src/train.py`):**
    *   Lê o dataset `data/SMSSpamCollection`.
    *   Cria um `Pipeline` do Scikit-learn que une o `TfidfVectorizer` (converte texto em números) ao `MultinomialNB` (algoritmo Naive Bayes).
    *   Salva o pipeline completo em `model.joblib`. O uso do `Pipeline` garante que o modelo em produção use exatamente o mesmo vocabulário do treino.

3.  **Carregamento e Inferência (`app/model_loader.py`):**
    *   Implementa o padrão Singleton: o modelo é carregado do disco apenas **uma vez** (na subida do servidor) para garantir baixa latência nas predições.
    *   A função `predict` recebe o texto bruto, chama `clean_text` e devolve o rótulo e a probabilidade calculada pelo modelo.

4.  **API (`app/main.py`):**
    *   Usa FastAPI para gerenciar requisições HTTP.
    *   Utiliza o mecanismo de `lifespan` para carregar o modelo de forma segura no início da execução.
    *   Valida as entradas usando modelos Pydantic, garantindo que a API não processe mensagens vazias ou inválidas.

---

## 🚀 Como Usar

### 💻 Execução Local

**1. Preparar o ambiente:**
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate | Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
```

**2. Treinar o modelo:**
Antes de subir a API, você deve gerar o artefato:
```bash
python -m src.train
```
Este comando treina o modelo e exibe métricas de acurácia no console.

**3. Rodar os testes:**
Garanta que a lógica de limpeza não foi quebrada:
```bash
pytest tests/ -v
```

**4. Iniciar o servidor:**
```bash
uvicorn app.main:app --reload
```
A API estará disponível em `http://localhost:8000`. Acesse `/docs` para ver o Swagger interativo.

### 🐳 Execução com Docker

O Docker garante que o ambiente de execução seja idêntico ao do desenvolvedor.
```bash
# Gere o modelo localmente antes do build
python -m src.train

# Build e Run
docker build -t spam-detection-api .
docker run -p 8000:8000 spam-detection-api
```

---

## 🔄 Pipeline CI/CD (GitHub Actions)

A pipeline automatizada garante a qualidade e entrega contínua do projeto. Ela está definida em `.github/workflows/main.yml` e funciona em dois jobs sequenciais:

### 1. Job: Test (Qualidade)
Sempre que há um **Push** ou **Pull Request** para a branch `main`:
*   O ambiente Python é montado.
*   As dependências são instaladas.
*   **O modelo é treinado do zero** no ambiente de CI.
*   **Os testes unitários são executados.** Se falharem, o pipeline para imediatamente.
*   O arquivo `model.joblib` gerado é salvo como um **Artifact** para ser usado no próximo job.

### 2. Job: Build and Push (Entrega)
Executado apenas se o job `Test` passar e se for um **Push direto na main**:
*   O artefato `model.joblib` é baixado.
*   O Docker realiza o build da imagem, injetando o modelo treinado.
*   A imagem é enviada para o **Docker Hub** com duas tags: `:latest` e o SHA do commit (para controle de versão).

**Segurança:** A pipeline utiliza `GitHub Secrets` (`DOCKERHUB_USERNAME` e `DOCKERHUB_TOKEN`) para ocultar credenciais sensíveis.

---

## 📊 Resultados do Modelo

| Métrica   | Ham   | Spam  |
|-----------|-------|-------|
| Precision | 0.95  | 1.00  |
| Recall    | 1.00  | 0.64  |
| F1-score  | 0.97  | 0.78  |
| Accuracy  | **95.25%** | — |

O modelo foca na **baixa taxa de falsos positivos** (Precision Spam = 1.0), garantindo que mensagens legítimas quase nunca sejam marcadas erroneamente como spam.
