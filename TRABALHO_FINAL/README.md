# Bank Marketing Subscription Predictor

Este projeto é uma solução completa de MLOps para prever se um cliente de uma instituição bancária irá subscrever a um depósito a prazo (investimento), com base em dados de campanhas de marketing direto.

## Cenário de Negócio

A conversão de vendas em depósitos a prazo é crucial para bancos aumentarem sua base de ativos. Utilizando o dataset **[Bank Marketing (UCI ID: 222)](https://archive.ics.uci.edu/dataset/222/bank+marketing)**, este projeto permite que a equipe de marketing foque seus esforços nos clientes com maior probabilidade de conversão, otimizando custos e aumentando a eficiência das chamadas telefônicas.

---

## Estrutura do Projeto

```text
bank_marketing_pro/
├── app/
│   ├── __init__.py
│   ├── main.py           # Servidor FastAPI com lifespan e endpoints
│   ├── schemas.py        # Contratos de entrada/saída com Pydantic
│   ├── model.py          # Carregamento, inferência e metadados do modelo
│   └── config.py         # Constantes e configurações centralizadas
├── models/               # Artefatos serializados (.joblib) gerados pelo treino
├── scripts/
│   └── train_model.py    # Pipeline de treino: extração, transformação e salvamento
├── tests/
│   ├── test_schemas.py   # Testes unitários dos schemas Pydantic
│   └── test_api.py       # Testes de integração dos endpoints FastAPI
├── Dockerfile            # Imagem Docker baseada em python:3.9-slim
├── requirements.txt      # Dependências fixadas para builds reproduzíveis
└── doc.md                # Documentação técnica da solução (preenchida pelo aluno)
```

---

## Como o Código Funciona

O projeto segue uma arquitetura modular que separa as fases de **treinamento**, **validação**, **testes** e **serviço**.

**1. Treinamento (`scripts/train_model.py`):**
- Baixa o dataset Bank Marketing diretamente do UCI via `ucimlrepo`.
- Aplica pré-processamento: encoding de variáveis categóricas, normalização numérica.
- Treina um `RandomForestClassifier` encapsulado em um `Pipeline` do Scikit-Learn.
- Salva o artefato em `models/bank_marketing_model.joblib` junto com metadados de métricas.

**2. Validação (`app/schemas.py`):**
- Define os contratos de entrada com `Pydantic v2` e `ConfigDict(extra="forbid")`.
- Valida tipos, ranges e valores categóricos antes de qualquer lógica de negócio.
- Impede campos desconhecidos, retornando HTTP 422 com mensagem clara.

**3. Carregamento e Inferência (`app/model.py`):**
- Implementa o padrão Singleton: o modelo é carregado do disco **uma única vez** na subida do servidor.
- Expõe funções para predição, verificação de status e metadados do modelo.

**4. API (`app/main.py`):**
- Usa FastAPI com `lifespan` para carregamento seguro do modelo na inicialização.
- Três endpoints: `/health`, `/info` e `/predict`.
- Retorna HTTP 503 se o modelo não estiver disponível.

---

## Endpoints da API

| Método | Endpoint   | Descrição                                      |
|--------|------------|------------------------------------------------|
| GET    | `/health`  | Verifica se a API está operacional             |
| GET    | `/info`    | Retorna metadados do modelo (algoritmo, features, métricas) |
| POST   | `/predict` | Recebe features do cliente e retorna a probabilidade de subscrição |

Acesse a documentação interativa em `http://localhost:8000/docs` (Swagger UI).

---

## Stack Tecnológica

| Biblioteca     | Uso                                      |
|----------------|------------------------------------------|
| FastAPI        | Servidor web de alta performance         |
| Pydantic v2    | Validação de dados e schemas da API      |
| Scikit-Learn   | Treinamento do modelo RandomForest       |
| UCIMLRepo      | Integração direta com o repositório UCI  |
| Joblib         | Serialização e desserialização do modelo |
| Pytest         | Testes unitários e de integração         |
| Docker         | Containerização para deploy consistente  |

---

## Como Executar

### Localmente

```bash
# 1. Instale as dependências
pip install -r requirements.txt

# 2. Treine o modelo (gera o artefato em models/)
python scripts/train_model.py

# 3. Execute os testes
pytest tests/ -v

# 4. Inicie a API
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

### Com Docker (Recomendado)

```bash
# 1. Treine o modelo localmente antes do build
python scripts/train_model.py

# 2. Construa a imagem
docker build -t bank-marketing-api .

# 3. Suba o container
docker run -p 8000:8000 bank-marketing-api
```

---

## Criterios de Avaliacao

### Criterios Principais (ate 10 pontos)

| Criterio                        | Descricao                                                                                              | Pontos |
|---------------------------------|--------------------------------------------------------------------------------------------------------|--------|
| Pipeline de Treinamento         | Script funcional que baixa dados, pre-processa, treina e salva o modelo com metricas registradas       | 2,0    |
| API FastAPI                     | Endpoints `/health`, `/info` e `/predict` funcionais com lifespan, tratamento de erros e HTTP corretos | 2,0    |
| Validacao com Pydantic          | Schemas com tipos, ranges, categorias validas e `extra="forbid"` nos campos de entrada                | 2,0    |
| Testes Automatizados            | Testes unitarios dos schemas e testes de integracao dos endpoints com pytest                          | 2,0    |
| Organizacao e Qualidade do Codigo | Estrutura modular, separacao de responsabilidades, sem codigo duplicado, PEP 8                       | 2,0    |
| **Total Principal**             |                                                                                                        | **10** |

### Criterios Bonus

| Criterio                   | Descricao                                                                              | Pontos |
|----------------------------|----------------------------------------------------------------------------------------|--------|
| Docker                     | Dockerfile funcional que constroi e executa a API corretamente em container isolado    | +3     |
| Documentacao da Solucao    | `doc.md` preenchido com arquitetura, decisoes tecnicas, validacao e estrategia de testes | +2   |
| **Total com Bonus**        |                                                                                        | **15** |

### Descricao Detalhada dos Criterios

**Pipeline de Treinamento (2,0 pts)**
- Download automatico do dataset via `ucimlrepo` ou fonte equivalente
- Pre-processamento correto (encoding, normalizacao)
- Treinamento com `Pipeline` do Scikit-Learn para garantir simetria treino-serving
- Salvamento do artefato em `models/` com joblib
- Exibicao de metricas ao final do treino (acuracia, F1, etc.)

**API FastAPI (2,0 pts)**
- Endpoint `GET /health` retornando status e versao do modelo
- Endpoint `GET /info` com metadados do modelo (algoritmo, features, metricas)
- Endpoint `POST /predict` recebendo features e retornando predicao com probabilidade
- Uso de `lifespan` para carregamento do modelo na inicializacao
- HTTP 503 quando modelo nao disponivel; HTTP 422 para entrada invalida

**Validacao com Pydantic (2,0 pts)**
- `BaseModel` com `ConfigDict(extra="forbid")` no schema de entrada
- Validacao de ranges numericos com `ge`/`le` nos campos `Field`
- Validacao de categorias com `Literal` ou `Enum`
- Schemas de resposta definidos para todos os endpoints

**Testes Automatizados (2,0 pts)**
- Testes unitarios dos schemas: campo valido, campo invalido, campo extra rejeitado
- Testes de integracao: `/health` retorna 200, `/predict` retorna predicao valida
- Testes negativos: payload invalido retorna 422, modelo ausente retorna 503
- Todos os testes passando com `pytest tests/ -v`

**Organizacao e Qualidade do Codigo (2,0 pts)**
- Separacao clara entre `app/`, `scripts/` e `tests/`
- Constantes em `config.py` — sem magic numbers espalhados no codigo
- Sem duplicacao de logica de pre-processamento entre treino e serving
- Codigo formatado conforme PEP 8 (sem erros de linting)

**Docker (+3 pts)**
- `Dockerfile` baseado em imagem slim com multi-stage ou camadas otimizadas
- Container sobe e responde corretamente em `localhost:8000`
- Modelo copiado/gerado corretamente dentro da imagem

**Documentacao da Solucao (+2 pts)**
- `doc.md` preenchido descrevendo a arquitetura da solucao
- Decisoes tecnicas justificadas (escolha do algoritmo, estrategia de validacao)
- Diagrama ou descricao do fluxo de dados do treino ao serving

---

## Entrega

1. **Destinatario:** lucasvpimentel@gmail.com
2. **Assunto:** `[Seu Nome Completo] - mlops`
3. **Conteudo:** Link do repositorio GitHub com a solucao completa.
4. **Data Limite:** **04 de abril de 2026**.

---

*Projeto desenvolvido para fins educacionais — MBA MLOps.*
