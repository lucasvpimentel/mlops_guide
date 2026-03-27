# MLOps: Da Experimentação à Produção

> **O que é MLOps?**
> MLOps (Machine Learning Operations) é o conjunto de práticas, ferramentas e cultura que une o desenvolvimento de modelos de Machine Learning com a operação de software em produção. O objetivo é levar modelos do notebook para o mundo real de forma confiável, reproduzível e sustentável.

---

## Por que MLOps Existe?

Imagine dois cenários:

**Sem MLOps:**
Uma cientista de dados treina um modelo de recomendação de filmes no seu notebook. O modelo funciona bem nos dados de teste. Ela envia o arquivo `.pkl` por e-mail para o time de engenharia. Três semanas depois, o modelo está em produção — mas ninguém sabe qual versão dos dados foi usada, com quais hiperparâmetros, ou por que a acurácia caiu 12% em relação ao notebook.

**Com MLOps:**
O mesmo modelo é treinado com um pipeline automatizado, cada experimento é rastreado, o artefato é versionado, a API é testada antes do deploy, e um dashboard avisa quando a distribuição dos dados muda em produção.

O problema não é ciência — é **engenharia**.

---

## Os Três Mundos do MLOps

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   DESENVOLVI-   │     │   EMPACOTA-     │     │    OPERAÇÃO     │
│    MENTO        │────▶│    MENTO        │────▶│   PRODUÇÃO      │
│                 │     │                 │     │                 │
│ • Exploração    │     │ • Serialização  │     │ • Serving       │
│ • Treinamento   │     │ • Containeriz.  │     │ • Monitoramento │
│ • Avaliação     │     │ • CI/CD         │     │ • Retreinamento │
└─────────────────┘     └─────────────────┘     └─────────────────┘
     Cientista                DevOps /               SRE /
     de Dados                 MLEngineer             Platform
```

---

## 1. Versionamento de Dados e Modelos

### O Problema
Em desenvolvimento de software tradicional, versionamos código com Git. Em ML, o comportamento do sistema depende de **três coisas**: código + dados + hiperparâmetros. Versionar só o código não é suficiente.

### Exemplo: GPT e Versionamento

Quando a OpenAI lançou `gpt-3.5-turbo`, depois `gpt-3.5-turbo-0301`, depois `gpt-3.5-turbo-0613` — cada sufixo de data é um **snapshot imutável** do modelo. Isso é MLOps na prática:

- `gpt-4` pode mudar silenciosamente ao longo do tempo
- `gpt-4-0613` é sempre o mesmo modelo, sempre o mesmo comportamento
- Aplicações críticas **apontam para versões fixas**, não para o alias mais recente

```python
# Ruim — comportamento pode mudar sem aviso
client.chat.completions.create(model="gpt-4")

# Bom — comportamento previsível e auditável
client.chat.completions.create(model="gpt-4-0613")
```

### No ML Clássico: MLflow e DVC

```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)
    mlflow.log_metric("accuracy", 0.94)
    mlflow.sklearn.log_model(model, "random_forest_v2")
```

Cada execução gera um `run_id` único. Meses depois, você consegue reproduzir exatamente aquele modelo.

---

## 2. Serialização de Modelos

### O que é Serialização?
Serialização é o processo de converter um objeto Python (o modelo treinado na memória) em um arquivo que pode ser salvo no disco e carregado depois — em outra máquina, em outro momento.

### Formatos Comuns

| Formato | Usado por | Características |
|---------|-----------|-----------------|
| `.joblib` | scikit-learn | Eficiente para arrays NumPy, padrão sklearn |
| `.pkl` (pickle) | Python geral | Universal, mas inseguro com código externo |
| `SavedModel` | TensorFlow/Keras | Contém arquitetura + pesos + grafo |
| `.pt` / `.pth` | PyTorch | State dict ou modelo completo |
| `GGUF` | LLMs locais (llama.cpp) | Modelos quantizados para rodar sem GPU |
| `ONNX` | Interoperabilidade | Roda em qualquer framework |

### Exemplo: Serialização de um Classificador

```python
import joblib
from sklearn.ensemble import RandomForestClassifier

# Treino
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Serialização: Python object → arquivo binário
artefato = {
    "pipeline": modelo,
    "feature_names": ["carat", "cut", "color", "clarity"],
    "version": "1.0.0",
    "metrics": {"rmse": 312.4, "r2": 0.98},
}
joblib.dump(artefato, "model/diamond_model.joblib")

# Desserialização: arquivo binário → Python object
artefato_carregado = joblib.load("model/diamond_model.joblib")
modelo_carregado = artefato_carregado["pipeline"]
preco = modelo_carregado.predict([[0.89, 2, 1, 3, 62.3, 57.0, 6.18, 6.21, 3.86]])
```

### Exemplo com LLM: Quantização como Serialização Especializada

Modelos de linguagem como o LLaMA 3 têm 8 bilhões de parâmetros. Em `float32`, isso ocupa ~32GB de RAM. A quantização é uma forma especial de serialização que comprime os pesos:

```
LLaMA 3 8B (float32):  ~32 GB  → inviável na maioria dos computadores
LLaMA 3 8B (int8):     ~8 GB   → roda em GPUs consumer
LLaMA 3 8B (Q4_K_M):   ~4.5 GB → roda em CPU com RAM suficiente
```

O arquivo `.gguf` é um formato de serialização que inclui tanto os pesos quantizados quanto metadados do modelo (arquitetura, tokenizer, contexto máximo).

---

## 3. Serving: Disponibilizando o Modelo

### O que é Model Serving?
Serving é expor o modelo como um serviço consumível — tipicamente uma API HTTP que recebe dados de entrada e retorna predições.

### Padrão: FastAPI + Singleton

O padrão mais importante no serving é carregar o modelo **uma única vez** na inicialização da aplicação e reutilizá-lo em todas as requisições. Carregar do disco a cada requisição seria ~100x mais lento.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
import joblib

_modelo = None  # Singleton global

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _modelo
    _modelo = joblib.load("model/diamond_model.joblib")  # 1x no startup
    yield  # API aceita requisições
    _modelo = None  # cleanup no shutdown

app = FastAPI(lifespan=lifespan)

@app.post("/predict")
def predict(features: DiamondFeatures):
    return _modelo["pipeline"].predict([features.to_array()])  # reutiliza
```

### Serving de LLMs: Ollama e vLLM

Para modelos generativos, o serving tem desafios adicionais:

```
ML clássico:  1 request → predição instantânea (~ms)
LLM:          1 request → geração token a token (~segundos)
              N requests simultâneos → batching dinâmico necessário
```

O **vLLM** resolve isso com *PagedAttention*: gerencia a memória KV-cache de múltiplas requisições em paralelo, como um sistema operacional gerencia memória virtual.

```python
# vLLM serve o mesmo modelo para múltiplos usuários simultaneamente
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Meta-Llama-3-8B-Instruct")  # carrega 1x
params = SamplingParams(temperature=0.7, max_tokens=512)

# Múltiplas requisições processadas em batch automaticamente
respostas = llm.generate(["Explique MLOps em 3 linhas"], params)
```

---

## 4. Validação de Dados e Schemas

### Por que Validar?
Um modelo treinado espera dados em um formato específico. Se a API aceitar dados inválidos, o modelo pode:
- Retornar predições absurdas silenciosamente
- Travar com erros internos não informativos
- Produzir resultados enviesados

### Pydantic: Contrato Explícito

```python
from pydantic import BaseModel, Field
from typing import Literal

class DiamondFeatures(BaseModel):
    carat: float = Field(..., ge=0.2, le=5.01)
    cut: Literal["Fair", "Good", "Very Good", "Premium", "Ideal"]
    color: Literal["D", "E", "F", "G", "H", "I", "J"]
    depth: float = Field(..., ge=43.0, le=79.0)

# Tentativa com dado inválido
try:
    DiamondFeatures(carat=100.0, cut="Perfeito", color="Z", depth=62.3)
except ValidationError as e:
    print(e)
    # carat: Input should be less than or equal to 5.01
    # cut: Input should be 'Fair', 'Good', 'Very Good', 'Premium' or 'Ideal'
    # color: Input should be 'D', 'E', 'F', 'G', 'H', 'I' or 'J'
```

### Validação em RAG (IA Generativa)

Em sistemas de Retrieval-Augmented Generation, a validação acontece em múltiplas camadas:

```
Usuário envia pergunta
        ↓
[Validação de entrada]    ← tamanho, caracteres, toxicidade
        ↓
[Retrieval]               ← busca documentos relevantes
        ↓
[Validação do contexto]   ← relevância mínima (score > 0.7)
        ↓
[LLM gera resposta]
        ↓
[Validação de saída]      ← alucinações, PII, conteúdo impróprio
        ↓
Resposta para o usuário
```

---

## 5. Containerização com Docker

### O Problema de Portabilidade
"Funciona na minha máquina" é o pesadelo do MLOps. Um modelo pode depender de:
- Versão específica do Python (3.10 vs 3.11)
- Versão do NumPy (1.24 vs 1.26 tem comportamentos diferentes)
- Bibliotecas do sistema operacional (CUDA, libgomp)
- Variáveis de ambiente

### Docker Resolve Isso

```dockerfile
# A imagem define o ambiente completo e reproduzível
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt  # versões fixas

COPY app/ ./app/
COPY model/ ./model/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Qualquer máquina com Docker roda isso identicamente
docker build -t meu-modelo .
docker run -p 8000:8000 meu-modelo
```

### Docker para LLMs: Ollama

O Ollama é essencialmente Docker para modelos de linguagem — empacota o modelo, o runtime e a API em um único artefato portável:

```bash
# Instala e roda LLaMA 3 em qualquer máquina com Docker
docker run -d -v ollama:/root/.ollama -p 11434:11434 ollama/ollama
docker exec -it <container> ollama run llama3

# API compatível com OpenAI disponível imediatamente
curl http://localhost:11434/api/generate \
  -d '{"model": "llama3", "prompt": "O que é MLOps?"}'
```

### Multi-stage Build: Separando Build de Runtime

```dockerfile
# Estágio 1: instala dependências (camada pesada, cacheada)
FROM python:3.11-slim AS builder
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Estágio 2: imagem final enxuta (sem ferramentas de build)
FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages \
                    /usr/local/lib/python3.11/site-packages
COPY app/ ./app/
COPY model/ ./model/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

A imagem final pode ser **3-5x menor** que uma imagem single-stage equivalente.

---

## 6. CI/CD para Machine Learning

### O que é CI/CD?
- **CI (Continuous Integration)**: a cada push, o código é automaticamente testado
- **CD (Continuous Delivery)**: se os testes passam, o modelo pode ser deployed automaticamente

### GitHub Actions: Exemplo Completo

```yaml
# .github/workflows/ml-pipeline.yml
name: ML Pipeline

on:
  push:
    branches: [main]
  pull_request:

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Lint com Flake8
        run: flake8 app/ train/ tests/ --max-line-length=100

      - name: Testes unitários
        run: pytest tests/test_schemas.py -v

      - name: Treinar modelo
        run: python train/train.py

      - name: Testes de integração
        run: pytest tests/test_api.py -v

      - name: Build Docker image
        run: docker build -t meu-modelo:${{ github.sha }} .
```

### CI/CD para Fine-tuning de LLMs

Em pipelines de LLM, o CI/CD vai além de testes de código:

```
Push de novos dados de treinamento
        ↓
[CI] Validação do dataset     ← formato, distribuição, toxicidade
        ↓
[CI] Fine-tuning automático   ← LoRA/QLoRA em GPU runner
        ↓
[CI] Avaliação automática     ← benchmarks MMLU, HellaSwag, etc.
        ↓
[CD] Se métricas melhoraram:  ← deploy canário (5% do tráfego)
        ↓
[CD] Aprovação humana         ← revisão das amostras geradas
        ↓
[CD] Rollout completo         ← substituição do modelo anterior
```

---

## 7. Monitoramento e Data Drift

### O Problema: Modelos Envelhecem

Um modelo é uma fotografia do mundo no momento do treino. O mundo muda. Os dados mudam. O modelo não.

Exemplos reais:
- Modelo de detecção de fraude treinado pré-COVID → padrões de compra mudaram completamente
- LLM treinado até 2023 → não sabe de eventos de 2024
- Modelo de previsão de demanda → não antecipa uma pandemia

### Tipos de Drift

```
Data Drift (Covariate Shift):
  Treino: usuários principalmente 25-40 anos
  Produção: novos usuários 60+ anos (comportamento diferente)

Concept Drift:
  Treino: "banco" significa instituição financeira
  Produção: "banco" começa a ser usado para app de pagamento

Label Drift:
  Treino: spam era e-mails com "Ganhe dinheiro rápido"
  Produção: spam evoluiu para técnicas mais sofisticadas
```

### Monitoramento Prático

```python
# Prometheus + Grafana para métricas em tempo real
from prometheus_client import Counter, Histogram, Gauge

predictions_total = Counter("predictions_total", "Total de predições")
prediction_confidence = Histogram("prediction_confidence", "Distribuição de confiança")
model_loaded = Gauge("model_loaded", "1 se modelo carregado, 0 se não")

@app.post("/predict")
def predict(features: DiamondFeatures):
    result = model_module.predict(features)

    predictions_total.inc()
    prediction_confidence.observe(result.confidence)

    return result
```

### Detecção de Drift em LLMs

Para modelos generativos, o monitoramento é mais complexo:

```python
# Exemplos de métricas para APIs de LLM
metricas = {
    "latencia_p99_ms": 2340,           # tempo de resposta
    "tokens_por_segundo": 48,          # throughput de geração
    "taxa_recusa": 0.03,               # % de respostas recusadas por safety
    "comprimento_medio_resposta": 312, # tokens por resposta
    "score_relevancia": 0.87,          # avaliação automática com LLM-as-judge
    "hallucination_rate": 0.05,        # taxa de alucinações detectadas
}
```

---

## 8. Feature Store

### O Problema de Consistência

Imagine que você calcula a feature "média de compras dos últimos 30 dias" de um usuário:
- No treino: calculada sobre dados históricos do data warehouse
- Na produção: precisa ser calculada em tempo real para cada requisição

Se as implementações divergirem minimamente (diferentes fusos horários, arredondamentos, janelas de tempo), o modelo recebe features diferentes das que viu no treino. Isso se chama **training-serving skew**.

### Feature Store Resolve Isso

```
             ┌─────────────┐
             │  Feature    │
  Dados ────▶│   Store     │◀──── Pipeline de treino
  brutos     │             │
             │  (Feast,    │──── Pipeline de serving
             │   Tecton)   │
             └─────────────┘
             Uma fonte única de verdade
```

### Exemplo com Fashion MNIST

No exercício do Curador de Moda, o training-serving skew é a principal lição:

```python
# TREINO (train.py) — pré-processamento
X_train = imagens.reshape(-1, 784).astype(np.float32) / 255.0

# SERVING (model.py) — DEVE SER IDÊNTICO
def preprocess_image_bytes(image_bytes: bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert("L")           # grayscale
    image = image.resize((28, 28))       # 28x28
    arr = np.array(image, dtype=np.float32) / 255.0  # /255 — OBRIGATÓRIO
    return arr.flatten().reshape(1, -1)  # (1, 784)
```

Se o `/255.0` for omitido no serving, o modelo recebe pixels em [0, 255] em vez de [0, 1] — e toda predição estará errada.

---

## 9. Prompt Engineering como MLOps para IA Generativa

### LLMOps: A Nova Fronteira

Com LLMs, o "modelo" muitas vezes não é retreinado — ele é **guiado por prompts**. O gerenciamento de prompts tem os mesmos desafios de MLOps:

| MLOps clássico | LLMOps |
|----------------|--------|
| Versionar pesos do modelo | Versionar prompts de sistema |
| Avaliar com métricas numéricas | Avaliar com LLM-as-judge |
| Retreinar com novos dados | Refinar prompts com novos exemplos |
| A/B test de modelos | A/B test de prompts |
| Monitorar data drift | Monitorar drift de intenção do usuário |

### Versionamento de Prompts

```python
# prompts/v1.0.0.py
SYSTEM_PROMPT_V1 = """
Você é um assistente de moda. Classifique a peça de roupa descrita.
Responda apenas com o nome da categoria.
"""

# prompts/v1.1.0.py — melhorado após avaliação
SYSTEM_PROMPT_V1_1 = """
Você é um especialista em moda com 20 anos de experiência.
Ao classificar uma peça de roupa, considere o contexto cultural e a estação do ano.
Responda no formato JSON: {"categoria": "...", "confianca": 0.0-1.0, "justificativa": "..."}
"""
```

### Avaliação Automática com LLM-as-Judge

```python
import anthropic

def avaliar_resposta(pergunta: str, resposta: str, referencia: str) -> dict:
    """Usa Claude para avaliar a qualidade de uma resposta gerada."""
    client = anthropic.Anthropic()

    prompt = f"""
    Avalie a resposta abaixo em uma escala de 1-5 para:
    - Precisão factual (está correto?)
    - Relevância (responde à pergunta?)
    - Completude (cobre os pontos principais?)

    Pergunta: {pergunta}
    Resposta gerada: {resposta}
    Resposta de referência: {referencia}

    Responda em JSON: {{"precisao": X, "relevancia": X, "completude": X, "justificativa": "..."}}
    """

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
```

---

## 10. O Ciclo de Vida Completo de um Modelo

```
┌─────────────────────────────────────────────────────────────────┐
│                    CICLO DE VIDA MLOps                          │
│                                                                 │
│  1. PROBLEMA          2. DADOS             3. EXPERIMENTAÇÃO   │
│  ┌──────────┐        ┌──────────┐         ┌──────────┐        │
│  │ Definir  │───────▶│ Coletar  │────────▶│ Treinar  │        │
│  │ métricas │        │ Limpar   │         │ Avaliar  │        │
│  │ de neg.  │        │ Versionar│         │ Comparar │        │
│  └──────────┘        └──────────┘         └──────────┘        │
│                                                   │            │
│  6. MONITORAMENTO     5. PRODUÇÃO         4. EMPACOTAMENTO    │
│  ┌──────────┐        ┌──────────┐         ┌──────────┐        │
│  │ Drift    │◀───────│ Serving  │◀────────│ Docker   │        │
│  │ Alertas  │        │ Scaling  │         │ CI/CD    │        │
│  │ Retreino │        │ A/B test │         │ Testes   │        │
│  └──────────┘        └──────────┘         └──────────┘        │
│        │                                                        │
│        └────────────────────────────────────────────────────── │
│                    (volta ao passo 1 ou 3)                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Referências e Próximos Passos

### Ferramentas do Ecossistema MLOps

| Categoria | Ferramentas Open Source | SaaS/Cloud |
|-----------|------------------------|------------|
| Experiment tracking | MLflow, DVC | Weights & Biases, Neptune |
| Feature store | Feast, Hopsworks | Tecton, Vertex AI |
| Model registry | MLflow Registry | Hugging Face Hub, SageMaker |
| Serving | FastAPI, TorchServe, vLLM | Vertex AI, SageMaker Endpoints |
| Monitoramento | Prometheus + Grafana | Evidently, Arize |
| Orquestração | Airflow, Prefect | Vertex Pipelines, SageMaker Pipelines |
| Containerização | Docker, Kubernetes | EKS, GKE, AKS |
| CI/CD | GitHub Actions, GitLab CI | CircleCI, Jenkins |
| LLMOps | LangSmith, LlamaIndex | Langfuse, Helicone |

### Leituras Recomendadas

- **"Designing Machine Learning Systems"** — Chip Huyen (O'Reilly)
- **"Machine Learning Engineering"** — Andriy Burkov
- **"Building LLMs for Production"** — Towards AI
- **Google MLOps Whitepaper** — ml-ops.org
- **Hugging Face Course** — huggingface.co/learn

---

> **Resumo em uma frase**: MLOps é o que garante que um modelo que funciona no notebook continue funcionando — e melhorando — em produção, semanas, meses e anos depois.
