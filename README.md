<div align="center">

# 🤖 MLOps na Prática
### Do Notebook à Produção — Guia Completo da Disciplina

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)
![Pytest](https://img.shields.io/badge/Pytest-Tested-orange?style=for-the-badge&logo=pytest)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-black?style=for-the-badge&logo=githubactions)

</div>

---

## 🧭 O Problema que MLOps Resolve

> *"Um modelo de ML que só funciona no notebook não é um produto — é um experimento."*

```
❌  SEM MLOps                        ✅  COM MLOps
─────────────────────────────────    ─────────────────────────────────
 Notebook local                       Pipeline automatizado
 "Funciona na minha máquina"          Docker garante portabilidade
 Sem testes → bugs silenciosos        Pytest detecta erros cedo
 Modelo sem versão → caos             Artefato versionado (.joblib)
 Deploy manual e frágil               CI/CD automatiza o processo
 Dados inválidos → crash              Pydantic valida na entrada
```

---

## 🗺️ Jornada da Disciplina

```
  FUNDAMENTOS          EMPACOTAMENTO        QUALIDADE           AUTOMAÇÃO
──────────────────   ─────────────────   ─────────────────   ─────────────────

  Exercício 01         Exercício 03         Exercício 04         Exercício 05
  Validação Pydantic   Docker               Testes Unitários     GitHub Actions
  API com FastAPI      Containerização      Pytest               Linter (Flake8)

  Exercício 02         Exercício 06         Exercício 04         Exercício 07
  Serialização         Visão Computacional  Heart Disease        CI/CD Completo
  Joblib / Artefatos   Upload de Imagem     Validação Biol.      Spam Detection

──────────────────   ─────────────────   ─────────────────   ─────────────────
```

---

## 📚 Mapa dos Exercícios

| # | Projeto | Dataset | Foco MLOps | Técnicas |
|---|---------|---------|------------|----------|
| 01 | 🐧 Identificador de Pinguins | Palmer Penguins | **Validação de Dados** | FastAPI, Pydantic, Enums |
| 02 | ⚡ Eficiência Energética | UCI Energy | **Serialização de Modelos** | Joblib, Artefatos, Singleton |
| 03 | 💎 Preço de Diamantes | Diamonds | **Containerização** | Docker, Multi-stage Build |
| 04 | 🫀 Diagnóstico Cardíaco | Heart Disease UCI | **Testes Unitários** | Pytest, Validação Biológica |
| 05 | 🚗 Avaliação de Carros | Car Evaluation UCI | **Qualidade de Código** | GitHub Actions, Flake8 |
| 06 | 👗 Curador de Moda | Fashion MNIST | **Serialização de Imagens** | Upload de Arquivo, Streamlit |
| 07 | 📩 Detecção de Spam | SMS Spam UCI | **CI/CD Completo** | GitHub Actions, Docker, NLP |

---

## 🔬 Teoria Essencial

### O Ciclo de Vida de um Modelo em Produção

```
  ┌─────────────────────────────────────────────────────────────────────┐
  │                                                                     │
  │   1. DADOS          2. TREINO         3. ARTEFATO                  │
  │   ┌─────────┐       ┌─────────┐       ┌─────────┐                  │
  │   │ Coleta  │──────▶│ sklearn │──────▶│ .joblib │                  │
  │   │ Limpeza │       │ Pipeline│       │ + meta  │                  │
  │   │ Validar │       │ fit()   │       │ dados   │                  │
  │   └─────────┘       └─────────┘       └────┬────┘                  │
  │                                            │                        │
  │   6. MONITOR        5. PRODUÇÃO        4. DEPLOY                   │
  │   ┌─────────┐       ┌─────────┐       ┌────▼────┐                  │
  │   │  Drift  │◀──────│  API    │◀──────│ Docker  │                  │
  │   │ Alertas │       │ FastAPI │       │  Image  │                  │
  │   │Retreino │       │ /predict│       │         │                  │
  │   └─────────┘       └─────────┘       └─────────┘                  │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
```

### As 5 Camadas de uma API de ML

```
  REQUISIÇÃO HTTP
        │
        ▼
  ┌─────────────┐
  │   Pydantic  │  ← Camada 1: Validação de Entrada
  │  Schemas    │    "carat=99" → 422 Unprocessable Entity
  └──────┬──────┘
         │ dados válidos
         ▼
  ┌─────────────┐
  │  FastAPI    │  ← Camada 2: Roteamento e HTTP
  │  Endpoints  │    GET /health  POST /predict  GET /info
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │   model.py  │  ← Camada 3: Lógica de Inferência
  │  Singleton  │    Carregado 1x no startup, reutilizado sempre
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │  Pipeline   │  ← Camada 4: Pré-processamento + Modelo
  │  sklearn    │    Scaler → Encoder → Estimator
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │  Artefato   │  ← Camada 5: Serialização em Disco
  │  .joblib    │    { pipeline, features, metrics, version }
  └─────────────┘
```

### Training-Serving Symmetry — A Regra de Ouro

```
  TREINO (train.py)                 SERVING (model.py)
  ─────────────────────────         ─────────────────────────
  X = imagens / 255.0          ==   arr = array / 255.0
  X = X.reshape(-1, 784)       ==   arr = arr.reshape(1, -1)
  encoder.fit(categoricas)     ==   encoder.transform(categoricas)
  pipeline.fit(X_train, y)     →    pipeline.predict(X_novo)

  Se esta simetria for quebrada = Training-Serving Skew
  Resultado: predicoes incorretas sem nenhum erro explicito
```

---

## 🐧 Exercício 01 — O Identificador de Pinguins

**Dataset:** Palmer Penguins · **Foco:** Validação de Dados com Pydantic

```
  Usuário envia JSON
        │
        ▼
  ┌─────────────────────────────────────────────────────────┐
  │  PenguinFeatures (Pydantic)                             │
  │                                                         │
  │  bill_length_mm: float  ge=10.0  le=80.0  ok ou 422     │
  │  island: Enum           "Torgersen" | "Biscoe" | "Dream"│
  │  sex: Enum              "male" | "female"               │
  │  campo_extra:           ConfigDict(extra="forbid") 422  │
  └────────────────────────┬────────────────────────────────┘
                           │ dados válidos
                           ▼
                    RandomForest
                           │
                           ▼
              { species, confidence, probabilities }
```

**Conceito-chave:** Garbage In, Garbage Out — validar na entrada evita predições absurdas silenciosas.

---

## ⚡ Exercício 02 — Eficiência Energética

**Dataset:** UCI Energy Efficiency · **Foco:** Serialização com Joblib

```
  O que é um Artefato de Modelo?

  Salvar só o modelo:            Artefato completo:
  ──────────────────             ──────────────────────────────────
  joblib.dump(model, f)          joblib.dump({
                                     "pipeline":  pipeline,
                                     "features":  feature_names,
                                     "metrics":   {"rmse": 1.4, "r2": 0.98},
                                     "version":   "1.0.0",
                                 }, f)

  Vantagem: meses depois você ainda sabe o que esse modelo faz,
  quais dados usou e qual performance tinha no momento do treino.
```

```
  Singleton Pattern — carregar o modelo apenas 1 vez:

  Sem Singleton:                   Com Singleton (lifespan):
  ─────────────────────────        ─────────────────────────────────
  def predict(data):               _artifact = None
      model = joblib.load(...)
      return model.predict(data)   @asynccontextmanager
                                   async def lifespan(app):
  → ~200ms por request                 global _artifact
  → disco lido 1000x/dia               _artifact = joblib.load(...)
                                        yield
                                   → ~2ms por request
                                   → disco lido 1x no startup
```

---

## 💎 Exercício 03 — Previsão de Preço de Diamantes

**Dataset:** Diamonds (ggplot2) · **Foco:** Containerização com Docker

```
  O problema de portabilidade:

  Máquina A (Python 3.10):  ok  Funciona
  Máquina B (Python 3.12):  ❌  scikit-learn incompatível
  Servidor  (Ubuntu):       ❌  versão numpy diferente

  Com Docker:
  docker build -t diamond-api .
  docker run -p 8000:8000 diamond-api

  Resultado identico em Windows / Mac / Linux / AWS / GCP / Azure
```

```dockerfile
  Multi-stage Build — imagem mais enxuta:

  # Estágio 1: BUILDER (~800MB com ferramentas de build)
  FROM python:3.11-slim AS builder
  RUN pip install -r requirements.txt

  # Estágio 2: RUNTIME (~200MB, apenas o necessário)
  FROM python:3.11-slim
  COPY --from=builder /usr/local/lib/python3.11/site-packages .
  COPY app/ model/ ./
  CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🫀 Exercício 04 — Diagnóstico Cardíaco

**Dataset:** Heart Disease UCI · **Foco:** Testes Unitários com Pytest

```
  Por que testar uma API de ML?

  Sem testes:                         Com testes (Pytest):
  ─────────────────────────           ──────────────────────────────────
  idade = 150 anos → predição         idade = 150 → 422 Unprocessable
  colesterol = -10 → predição         colesterol = -10 → 422
  modelo nao carregado → crash        modelo nao carregado → 503 claro
  deploy silenciosamente quebrado     CI bloqueia deploy se falhar
```

```
  Pirâmide de Testes:
                    /\
                   /  \
                  / E2E \          ← Poucos, lentos, caros
                 /────────\
                / Integração\      ← test_api.py (TestClient)
               /──────────────\
              /   Unitários    \   ← test_schemas.py (puro Python)
             /──────────────────\
            Mais rápidos · Mais baratos · Mais numerosos
```

---

## 🚗 Exercício 05 — Avaliação de Carros

**Dataset:** Car Evaluation UCI · **Foco:** CI/CD com GitHub Actions + Flake8

```
  O que acontece a cada git push:

  git push origin main
       │
       ▼
  ┌──────────────────────────────────────────────────────┐
  │  GitHub Actions — .github/workflows/main.yml         │
  │                                                      │
  │  1. runner ubuntu-latest inicializa                  │
  │  2. pip install flake8 scikit-learn fastapi pytest   │
  │  3. flake8 app/ src/ tests/                          │
  │         ├── Indentação errada?    → FALHA  BLOQUEIA  │
  │         ├── Variável não usada?   → FALHA  BLOQUEIA  │
  │         ├── Linha muito longa?    → FALHA  BLOQUEIA  │
  │         └── Código limpo?         → PASSA            │
  │  4. pytest tests/                                    │
  │         └── Todos passam?         → MERGE LIBERADO   │
  └──────────────────────────────────────────────────────┘
```

---

## 👗 Exercício 06 — O Curador de Moda

**Dataset:** Fashion MNIST (Zalando) · **Foco:** Imagens em APIs + Streamlit

```
  O Caminho da Foto ao Modelo:

  foto.jpg (binario)
       │
       ▼  POST /predict/upload (multipart/form-data)
  ┌─────────────────────────────────────────────────────┐
  │  FastAPI: UploadFile = File(...)                     │
  │       │                                             │
  │       ▼  await file.read() → bytes                  │
  │  PIL.Image.open(BytesIO(bytes))                     │
  │       ▼  .convert("L")                              │
  │  Escala de cinza (1 canal)                          │
  │       ▼  .resize((28, 28))                          │
  │  28 x 28 pixels                                     │
  │       ▼  np.array / 255.0                           │
  │  Array float32 [0.0, 1.0]                           │
  │       ▼  .flatten().reshape(1, -1)                  │
  │  Shape (1, 784) pronto para o modelo                │
  └──────────────────┬──────────────────────────────────┘
                     ▼
           MLPClassifier.predict_proba()
                     ▼
        { category, confidence, probabilities }
```

**As 10 classes do Fashion MNIST:**

| Índice | Classe | Índice | Classe |
|--------|--------|--------|--------|
| 0 | 👕 Camiseta/Top | 5 | 👡 Sandália |
| 1 | 👖 Calça | 6 | 👔 Camisa |
| 2 | 🧥 Pullover | 7 | 👟 Tênis |
| 3 | 👗 Vestido | 8 | 👜 Bolsa |
| 4 | 🧣 Casaco | 9 | 👢 Bota |

---

## 📩 Exercício 07 — Detecção de Spam

**Dataset:** SMS Spam UCI · **Foco:** CI/CD Completo + NLP

```
  Pipeline CI/CD Completo:

  Desenvolvedor          GitHub Actions              Produção
  ─────────────          ──────────────────          ──────────────
  Escreve código
       │
       ▼
  git push ────────────▶ Lint (Flake8)  ── Falha → BLOQUEIA
                              │
                              ▼
                         Testes (pytest) ─ Falha → BLOQUEIA
                              │
                              ▼
                         Build Docker ──── Falha → BLOQUEIA
                              │
                              ▼
                         Tudo passou ────────────────────────▶ Deploy
```

---

## 🛠️ Stack Tecnológica

```
  CAMADA          FERRAMENTA          FUNÇÃO
  ──────────────────────────────────────────────────────────────────
  API             FastAPI             Servidor HTTP assíncrono
  Validação       Pydantic v2         Schemas, tipos, constraints
  ML              scikit-learn        Treino, pipelines, métricas
  Serialização    Joblib              Salvar/carregar artefatos
  Imagens         Pillow (PIL)        Decode, resize, normalize
  Containers      Docker              Portabilidade total
  Testes          Pytest              Unitários e integração
  Qualidade       Flake8              Linting, estilo de código
  CI/CD           GitHub Actions      Automação de pipeline
  UI              Streamlit           Interface de demonstração
  Dados           seaborn / ucimlrepo Datasets públicos
```

---

## 📊 Comparativo dos Exercícios

| # | Tipo de ML | Algoritmo | Entrada | Saída |
|---|-----------|-----------|---------|-------|
| 01 Pinguins | Classificação | RandomForest | JSON 6 features | Espécie + probabilidades |
| 02 Energia | Regressão | GradientBoosting | JSON 8 features | kWh/m² |
| 03 Diamantes | Regressão | RandomForest | JSON 9 features | Preço em USD |
| 04 Coração | Classificação | RandomForest | JSON 13 features | Risco cardíaco (0/1) |
| 05 Carros | Classificação | RandomForest | JSON 6 features | unacc / acc / good |
| 06 Moda | Classificação | MLPClassifier | Imagem 28×28 | Categoria de roupa |
| 07 Spam | Classificação | Naive Bayes | Texto SMS | spam / ham |

---

## 🚀 Como Executar Qualquer Exercício

```bash
# 1. Entre na pasta do exercício
cd exercicio_01   # (ou 02, 03, 04, 05, 06, 07)

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Treine o modelo
python train/train.py

# 5. Inicie a API
uvicorn app.main:app --reload

# 6. Acesse a documentação interativa
#    http://localhost:8000/docs

# 7. Execute os testes
pytest tests/ -v
```

**Via Docker (exercícios 03+):**

```bash
# Após treinar o modelo:
docker build -t meu-exercicio .
docker run -p 8000:8000 meu-exercicio
# http://localhost:8000/docs
```

---

## 📁 Estrutura Padrão de Todos os Exercícios

```
exercicio_XX/
│
├── app/
│   ├── config.py      ← Constantes e caminhos (única fonte de verdade)
│   ├── schemas.py     ← Contratos Pydantic (entrada e saída)
│   ├── model.py       ← Singleton + lógica de inferência
│   └── main.py        ← Endpoints FastAPI + lifespan
│
├── train/
│   └── train.py       ← Carrega dados → treina → salva artefato
│
├── model/             ← Artefatos gerados (ignorados pelo git)
│   └── modelo.joblib
│
├── tests/
│   ├── test_schemas.py  ← Testes unitários (sem modelo necessário)
│   └── test_api.py      ← Testes de integração (com modelo)
│
├── Dockerfile         ← Containerização
├── requirements.txt   ← Dependências com versões fixadas
├── TEORIA.md          ← Conceitos MLOps do exercício
└── INSTRUCOES.md      ← Passo a passo de execução
```

---

## 💡 Glossário MLOps

| Termo | Definição |
|-------|-----------|
| **Artefato** | Arquivo `.joblib` com pipeline + metadados (features, métricas, versão) |
| **Singleton** | Modelo carregado 1x no startup e reutilizado em todas as requisições |
| **Schema** | Contrato de dados com validação automática (Pydantic) |
| **Lifespan** | Hook de startup/shutdown do FastAPI moderno |
| **Training-Serving Skew** | Divergência entre pré-processamento no treino e no serving |
| **Data Drift** | Mudança na distribuição dos dados em produção ao longo do tempo |
| **CI/CD** | Automação de teste e deploy a cada commit |
| **Multi-stage Build** | Docker em 2 etapas — imagem final sem ferramentas de build |
| **Linting** | Análise estática de código para detectar erros de estilo e bugs |
| **Feature Store** | Repositório centralizado de features para garantir consistência |

---

## 📚 Referências Consolidadas

### Datasets (Fontes Originais)
*   **Ex 01 (Pinguins):** Horst, A.M., Hill, A.P., & Gorman, K.B. (2020). *palmerpenguins: Palmer Archipelago (Antarctica) penguin data*. [R package version 0.1.0](https://allisonhorst.github.io/palmerpenguins/).
*   **Ex 02 (Energia):** Tsanas, A., & Xifara, A. (2012). *Accurate quantitative estimation of the energy performance of residential buildings using multi-output regression*. Energy and Buildings. [UCI Repository](https://archive.ics.uci.edu/dataset/242/energy+efficiency).
*   **Ex 03 (Diamantes):** Wickham, H. (2016). *ggplot2: Elegant Graphics for Data Analysis*. Springer-Verlag New York. [Diamonds documentation](https://ggplot2.tidyverse.org/reference/diamonds.html).
*   **Ex 04 (Coração):** Detrano, R. et al. (1989). *International application of a new probability algorithm for the diagnosis of coronary artery disease*. American Journal of Cardiology. [UCI Repository](https://archive.ics.uci.edu/dataset/45/heart+disease).
*   **Ex 05 (Carros):** Bohanec, M., & Rajkovic, V. (1990). *Expert system for decision making*. Sistemica. [UCI Repository](https://archive.ics.uci.edu/dataset/19/car+evaluation).
*   **Ex 06 (Moda):** Xiao, H., Rasul, K., & Vollgraf, R. (2017). *Fashion-MNIST: a Novel Image Dataset for Benchmarking Machine Learning Algorithms*. [arXiv:1708.07747](https://arxiv.org/abs/1708.07747).
*   **Ex 07 (Spam):** Almeida, T.A., Hidalgo, J.M.G., & Yamakami, A. (2011). *Contributions to the Study of SMS Spam Filtering: New Collection and Results*. ACM Symposium on Document Engineering (DocEng'11). [UCI Repository](https://archive.ics.uci.edu/dataset/228/sms+spam+collection).

### Tecnologias e Frameworks
*   **FastAPI:** [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) - Framework web de alta performance.
*   **Scikit-Learn:** [scikit-learn.org](https://scikit-learn.org/) - Machine Learning em Python.
*   **Pydantic:** [pydantic.dev](https://pydantic.dev/) - Validação de dados via Python type hints.
*   **Docker:** [docker.com](https://www.docker.com/) - Plataforma de containerização.
*   **Pytest:** [pytest.org](https://pytest.org/) - Framework de testes automatizados.
*   **Flake8:** [flake8.pycqa.org](https://flake8.pycqa.org/) - Ferramenta de linting e estilo (PEP 8).
*   **MLOps Theory:** Treveil, M. et al. (2021). *Introducing MLOps*. O'Reilly Media.

---

<div align="center">

**Para teoria aprofundada com exemplos de IA Generativa:** [`mlops.md`](mlops.md)

---

*Pós-Graduação · MLOps na Prática*

</div>
