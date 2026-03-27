# PLAN: Exercício 05 — Avaliação de Compra de Carros (Foco: Linting)

## 📌 Objetivo
Desenvolver uma API de classificação para aceitabilidade de carros, com foco na **Qualidade de Código e Padronização PEP 8** através do uso de Linters (Flake8).

## 🛠️ Stack Tecnológica
- **Linguagem:** Python 3.11+
- **Modelagem:** Scikit-Learn (RandomForestClassifier).
- **API:** FastAPI + Uvicorn.
- **Linting:** Flake8.
- **Automação:** GitHub Actions (Workflow de QA).

---

## 📋 Passo a Passo

### Fase 1: Estrutura e Treinamento
1. **[ ] Criar `requirements.txt`:** Incluir `fastapi`, `uvicorn`, `scikit-learn`, `pandas`, `joblib`, `ucimlrepo`, `flake8`.
2. **[ ] Desenvolver `train/train.py`:**
   - Baixar dataset Car Evaluation (UCI ID: 19).
   - Realizar pré-processamento (OneHotEncoder para as 6 features categóricas).
   - Treinar o modelo e salvar o `artifact` em `model/car_model.joblib`.

### Fase 2: Desenvolvimento da API
3. **[ ] Desenvolver `app/config.py`:** Definir as categorias válidas para cada feature (`buying`, `maint`, `doors`, `persons`, `lug_boot`, `safety`).
4. **[ ] Desenvolver `app/schemas.py`:** Criar schemas Pydantic com `Literal` para restringir os valores categóricos.
5. **[ ] Desenvolver `app/model.py`:** Lógica de carregamento do artefato e inferência.
6. **[ ] Desenvolver `app/main.py`:** Endpoints da API.

### Fase 3: Qualidade de Código (Linting)
7. **[ ] Configurar `.flake8`:** Definir regras de estilo (ex: max-line-length=88).
8. **[ ] Executar Flake8 localmente:** Corrigir eventuais violações de estilo.
9. **[ ] Criar Workflow GitHub Actions:** Definir um arquivo `.github/workflows/lint.yml` (ilustrativo para este exercício) que execute o `flake8` em todo o código.

### Fase 4: Documentação
10. **[ ] Criar `README.md`, `TEORIA.md` e `INSTRUCOES.md`:** 
    - Focar na importância de manter o código limpo para que a esteira de MLOps não quebre por erros triviais de estilo.

---

## 🎯 Critérios de Aceite
1. O comando `flake8 .` deve retornar zero erros.
2. A API deve validar rigorosamente as categorias de entrada (ex: rejeitar `buying="expensive"` em vez de `buying="high"`).
3. O projeto deve seguir o padrão de pastas estabelecido.
4. Documentação completa e clara.
