# Cadeia de Prompts — Identificador de Pinguins (Exercicio 01)

Esta sequência guia uma IA na criação de uma API de classificação, focando em validação e organização.

---

## 1. Setup, Dados e Estrutura
**Prompt:**
> "Quero criar um projeto de MLOps para classificar espécies de pinguins. Os dados devem ser extraídos da biblioteca `seaborn` usando `sns.load_dataset('penguins')`. 
> 
> Me ajude a configurar o `requirements.txt` (FastAPI, Uvicorn, Scikit-Learn, Pandas, Seaborn, Joblib, Pytest) e escolha uma das duas estruturas de pastas abaixo para organizar o projeto (me diga qual escolheu):
>
> **Opção A (Modular):**
> - `app/`: Contém `main.py`, `schemas.py`, `model_loader.py`.
> - `train/`: Contém `train_model.py`.
> - `model/`: Pasta para o arquivo `.joblib`.
> - `tests/`: Pasta para testes unitários e integração.
>
> **Opção B (Simples/Flat):**
> - `api.py`: Código da API.
> - `train.py`: Código de treino.
> - `models/`: Pasta para artefatos.
> - `tests/`: Pasta para testes."

**Por que:** 
Definir a fonte de dados e a estrutura logo no início evita que a IA crie arquivos em locais aleatórios, garantindo que o código de treino saiba exatamente onde salvar o modelo para a API ler depois.

---

## 2. Script de Treinamento
**Prompt:**
> "Escreva o script de treinamento (baseado na estrutura escolhida). O script deve carregar os dados do Seaborn, tratar valores nulos, converter as colunas 'island' e 'sex' para números e treinar um `RandomForestClassifier`. Salve o modelo final como `penguin_classifier.joblib` na pasta de modelos."

**Por que:**
O treinamento gera o "cérebro" da aplicação. Especificar o tratamento de nulos e a conversão de categorias garante que o modelo seja robusto.

---

## 3. Contratos de Dados (Schemas)
**Prompt:**
> "Crie os schemas Pydantic. A entrada deve validar que `body_mass_g` está entre 500 e 10.000 e que as strings de 'island' e 'sex' pertencem aos valores encontrados no dataset original. A saída deve retornar a espécie e a confiança da predição."

**Por que:**
Validação rigorosa impede que dados "sujos" cheguem ao modelo, o que causaria erros de predição ou quebras no sistema.

---

## 4. API e Endpoints
**Prompt:**
> "Desenvolva a API FastAPI. Ela deve carregar o modelo `.joblib` uma única vez no startup. Crie um endpoint POST `/predict` que use o schema de entrada e retorne a predição. Adicione também um endpoint GET `/health` para monitoramento."

**Por que:**
Carregar o modelo no startup é uma prática de performance: o modelo fica na memória RAM, tornando as predições instantâneas.

---

## 5. Testes e Docker
**Prompt:**
> "Crie um teste unitário para validar o schema de entrada e um `Dockerfile` baseado em `python:3.9-slim` que exponha a porta 8000 e rode a API usando Uvicorn."

**Por que:**
Testes validam a lógica e o Docker garante que qualquer pessoa consiga rodar o seu projeto sem precisar configurar o Python localmente.
