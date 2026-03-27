# PROMPTS: Exercício 05 — Avaliação de Carros

Este exercício foca na qualidade do código e na automação de processos de revisão via Linter.

---

## 1. Setup e Estrutura
**Prompt:**
> "Quero criar um projeto de MLOps para avaliar carros usando o dataset 'Car Evaluation' da UCI (ID 19). Me ajude com o `requirements.txt` (FastAPI, Scikit-Learn, Joblib, Pandas, ucimlrepo, flake8) e escolha uma estrutura modular para as pastas `app/`, `src/` e `models/`."

---

## 2. Treino com Encoding Ordinal
**Prompt:**
> "Crie um script `src/train.py` que baixe o dataset da UCI. Como os dados são categóricos ordinais (ex: vhigh, high, med, low), use o `OrdinalEncoder` do Scikit-Learn para manter a ordem lógica antes de treinar um `RandomForestClassifier`. Salve o modelo em `models/car_model.joblib`."

---

## 3. Schemas com Enums
**Prompt:**
> "Crie em `app/schemas.py` modelos Pydantic usando Enums para restringir as entradas aos valores aceitos pelo dataset (ex: buying: low, med, high, vhigh). Isso garante que o usuário não envie dados fora do domínio."

---

## 4. API de Predição
**Prompt:**
> "Desenvolva a API FastAPI em `app/main.py`. Ela deve carregar o modelo serializado e ter um endpoint POST `/predict`. Garanta que o código esteja bem formatado e sem variáveis não utilizadas para passar no linter."

---

## 5. Automação de Qualidade (Linter)
**Prompt:**
> "Crie um GitHub Action em `.github/workflows/linter.yml` que rode o `flake8` sempre que houver um push. O robô deve avisar se houver erros de indentação ou imports não utilizados."
