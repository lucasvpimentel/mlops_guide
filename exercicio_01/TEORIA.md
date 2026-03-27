# Teoria — Conceitos MLOps aplicados neste projeto

Este documento explica os conceitos de MLOps que estruturam o exercício do Identificador de Pinguins. O objetivo não é só fazer o modelo funcionar, mas fazê-lo funcionar de forma **confiável, auditável e sustentável**.

---

## 1. O que é MLOps?

MLOps (Machine Learning Operations) é um conjunto de práticas que une o desenvolvimento de modelos de ML com operações de software (DevOps). O problema central que ele resolve: **modelos que funcionam no notebook do cientista frequentemente falham em produção** — por dados inesperados, dependências não rastreadas, falta de monitoramento ou ausência de contratos claros.

MLOps não é uma ferramenta única. É uma disciplina que engloba:

| Área | Pergunta que responde |
|------|----------------------|
| Validação de dados | "O dado que chegou é o que eu espero?" |
| Model serving | "Como disponibilizo o modelo para ser usado?" |
| Reprodutibilidade | "Consigo recriar exatamente o mesmo resultado?" |
| Monitoramento | "O modelo continua funcionando bem em produção?" |
| Versionamento | "Qual versão do modelo está rodando agora?" |

Este exercício foca nos três primeiros.

---

## 2. Validação de Dados com Pydantic

### O problema
Um modelo de ML recebe um array numérico. Ele não sabe — nem se importa — se `body_mass_g = -500` faz sentido no mundo real. Vai calcular e retornar algo de qualquer forma. Isso é um **silent failure**: o sistema não quebra, mas produz um resultado inválido.

### A solução: contratos de dados
Um **contrato de dados** é uma especificação formal do que pode entrar no sistema. Com Pydantic, esse contrato é expresso diretamente no código Python como um schema com tipos e regras:

```python
body_mass_g: float = Field(..., ge=500.0, le=10_000.0)
```

Isso garante:
- **Tipo correto** (`float`, não `string`)
- **Valor mínimo** (`ge=500.0` — maior ou igual a 500, nunca negativo)
- **Valor máximo** (`le=10_000.0` — limite físico realista)
- **Documentação automática** — o schema é exposto no Swagger/OpenAPI

### Por que não validar na mão?
Validação manual (`if value < 0: raise ...`) é repetitiva, fácil de esquecer e não gera documentação. Pydantic torna a validação **declarativa**, **legível** e **automática**.

### Regras físicas vs. regras de negócio
Neste projeto usamos **regras físicas** — limites que derivam da biologia dos pinguins:

| Feature | Limite inferior | Limite superior | Motivo |
|---------|----------------|----------------|--------|
| `body_mass_g` | 500 g | 10.000 g | Pinguins existentes variam de ~1 kg (menor espécie) a ~40 kg (pinguim-imperador). Margem conservadora. |
| `bill_length_mm` | 10 mm | 80 mm | Bicos de pinguins palmípedes do dataset variam de ~32 mm a ~60 mm. |
| `flipper_length_mm` | 100 mm | 300 mm | Nadadeiras entre ~170 mm e ~230 mm no dataset original. |

Rejeitar dados fora dessas faixas **antes** de chegar ao modelo é uma prática de MLOps chamada **input validation gate**.

---

## 3. Model Serving com FastAPI

### O que é model serving?
Model serving é o processo de disponibilizar um modelo treinado como um serviço consumível por outros sistemas. Em vez de um script que roda uma vez, o modelo fica disponível 24/7 como uma API REST.

### Por que FastAPI?
FastAPI é a escolha moderna para model serving em Python porque:
- **Alta performance** — baseado em Starlette e Uvicorn (ASGI)
- **Integração nativa com Pydantic** — validação automática dos contratos
- **Documentação automática** — gera Swagger UI e ReDoc sem código extra
- **Async-ready** — suporta I/O assíncrono para alta concorrência

### Separação de responsabilidades
O projeto segue uma divisão clara de camadas:

```
main.py      → HTTP (rotas, status codes, tratamento de erros HTTP)
schemas.py   → Contratos (o que pode entrar e sair)
model.py     → Lógica de ML (transformação, predição)
config.py    → Configuração (paths, constantes)
```

Essa separação facilita **testes unitários** (cada camada testada isoladamente) e **manutenção** (mudar o modelo não afeta as rotas, mudar as rotas não afeta a lógica de ML).

### O padrão Singleton para o modelo
Carregar um modelo do disco é uma operação cara (leitura de arquivo, desserialização). Por isso, o modelo é carregado **uma única vez** no startup da API e mantido em memória:

```python
# Startup: carrega uma vez
@asynccontextmanager
async def lifespan(app):
    model_module.load_model()
    yield

# Predição: usa o modelo já em memória
def predict(features):
    return _artifact["pipeline"].predict(X)
```

Isso garante **latência baixa** por requisição — o modelo não é recarregado a cada chamada.

---

## 4. Reprodutibilidade e Artefatos

### O problema da reprodutibilidade
Se você treina um modelo hoje e re-treina amanhã com o mesmo código mas sem fixar a semente aleatória, pode obter resultados diferentes. Isso dificulta depuração e auditoria.

### Como garantir reprodutibilidade
1. **`random_state=42`** — semente fixa em todas as operações estocásticas (split, Random Forest)
2. **`requirements.txt` com versões fixadas** — `scikit-learn==1.4.2`, não `scikit-learn>=1.0`
3. **Separação treino/inferência** — o script `train/train_model.py` é separado da API. O artefato gerado (`.joblib`) é o único ponto de contato

### O artefato de modelo
O modelo serializado (`penguin_classifier.joblib`) contém não apenas os pesos do modelo, mas um **pipeline completo**:

```
Pipeline
├── StandardScaler  ← normalização dos dados
└── RandomForestClassifier  ← o classificador
```

Isso garante que a **mesma transformação usada no treino** seja aplicada na inferência — um erro clássico em ML é escalar os dados no treino mas não na produção.

---

## 5. Endpoints de Saúde e Observabilidade

### Por que `/health` e `/info`?
Em produção, sistemas externos (load balancers, orquestradores como Kubernetes) precisam saber se o serviço está saudável. O endpoint `/health` responde a essa pergunta:

```json
{"status": "ok", "model_loaded": true, "version": "1.0.0"}
```

Se `model_loaded` for `false`, o orquestrador pode reiniciar o container automaticamente.

O endpoint `/info` serve à **observabilidade** — permite auditar qual versão do modelo está rodando e quais features ele espera, sem precisar acessar o código-fonte.

### O que seria o próximo passo (além deste exercício)
| Prática | Ferramenta típica |
|---------|------------------|
| Rastreamento de experimentos | MLflow, W&B |
| Versionamento de modelos | MLflow Model Registry |
| Monitoramento de drift | Evidently, Whylogs |
| CI/CD para modelos | GitHub Actions + DVC |
| Containerização em produção | Docker + Kubernetes |

Este exercício implementa a base: **contrato de dados + serving + observabilidade básica**. As práticas acima constroem sobre essa fundação.
