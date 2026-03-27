# PROMPTS: Exercício 03 — Previsão de Diamantes

Este projeto enfatiza o uso de Pipelines de Scikit-Learn e conteinerização obrigatória.

---

## 1. Fonte de Dados e Pipeline
**Prompt:**
> "Quero prever o preço de diamantes usando o dataset 'diamonds' do Seaborn. O projeto deve usar um Scikit-Learn Pipeline com `OneHotEncoder` para a coluna 'cut' e um `RandomForestRegressor`. Me ajude com a estrutura modular em `app/`, `train/` e `model/`."

---

## 2. Script de Treino com Pipeline
**Prompt:**
> "Crie o script `train/train.py` para carregar o dataset do Seaborn, construir o Pipeline e salvar o objeto inteiro (pré-processamento + modelo) como `model/diamond_model.joblib`."

---

## 3. API e Docker
**Prompt:**
> "Desenvolva a API FastAPI em `app/main.py`. Crie também um `Dockerfile` baseado em `python:3.11-slim` que instale os `requirements.txt`, copie o modelo gerado e rode o servidor na porta 8000."
