# Cadeia de Prompts — Detector de Spam e CI/CD (Exercicio 07)

Este é o projeto consolidado. Ele une Machine Learning, Engenharia de Software e Automação de Infraestrutura (DevOps).

---

## 1. Fonte de Dados e Estrutura Robusta
**Prompt:**
> "Quero criar um sistema completo de detecção de Spam SMS. O dataset deve ser o 'SMS Spam Collection' da UCI (pode ser baixado via URL ou carregado de um CSV local). 
> 
> Me ajude com o `requirements.txt` (FastAPI, Scikit-Learn, Pandas, Joblib, Pytest, HTTPX) e escolha uma das estruturas abaixo para garantir um projeto profissional:
>
> **Opção A (Arquitetura Limpa):**
> - `app/`: Contém `main.py` e `model_loader.py` (serviço).
> - `src/`: Contém `preprocessing.py` (limpeza) e `train.py` (treino).
> - `tests/`: Pasta para testes unitários da limpeza e integração da API.
> - `.github/workflows/`: Pasta para o pipeline de CI/CD.
>
> **Opção B (Estrutura por Componente):**
> - `api/`: Todo o código FastAPI.
> - `ml/`: Scripts de treino e pré-processamento.
> - `tests/`: Testes automatizados.
> - `.github/workflows/`: Configurações de automação."

**Por que:** 
A separação entre `src/` (lógica de ML) e `app/` (serviço web) é uma prática recomendada para evitar que dependências de treino "poluam" o ambiente de produção.

---

## 2. Limpeza de Texto e Treino (Pipeline)
**Prompt:**
> "Crie uma função de limpeza de texto em `preprocessing.py` que remova pontuação e converta para minúsculas. Em `train.py`, use o `TfidfVectorizer` e o `MultinomialNB` dentro de um `Pipeline` do Scikit-Learn. Treine o modelo com o dataset de Spam e salve como `model.joblib`."

**Por que:**
O Naive Bayes (MultinomialNB) é o padrão ouro para classificação de texto simples. Usar o `Pipeline` garante que a transformação TF-IDF seja idêntica no treino e na API.

---

## 3. API com Padrão Singleton
**Prompt:**
> "Desenvolva a API FastAPI. Utilize o evento `lifespan` para carregar o modelo apenas uma vez. O endpoint `/predict` deve receber uma mensagem de texto, passar pela função de limpeza e retornar se é 'spam' ou 'ham', junto com a probabilidade."

**Por que:**
O padrão Singleton (carregar uma vez) evita que a API fique lenta ao ler o disco em cada mensagem recebida.

---

## 4. Testes Unitários de Lógica
**Prompt:**
> "Escreva testes em Pytest para a função de limpeza de texto. Garanta que ela lida corretamente com espaços extras, letras maiúsculas e caracteres especiais. Adicione também um teste que verifique se o modelo carregado retorna uma predição válida."

**Por que:**
Em CI/CD, os testes são os "portões de segurança". Se a limpeza de texto mudar, o modelo pode parar de funcionar; os testes detectam isso antes do deploy.

---

## 5. Dockerfile de Produção
**Prompt:**
> "Crie um `Dockerfile` que instale apenas o necessário para rodar a API. O arquivo deve copiar o modelo pré-treinado e expor a porta 8000."

**Por que:**
O Docker isola a aplicação, garantindo que ela rode da mesma forma no GitHub Actions e no servidor final.

---

## 6. Automação com GitHub Actions (CI/CD)
**Prompt:**
> "Crie um arquivo `.github/workflows/main.yml` que: 
> 1. Rode os testes sempre que houver um push.
> 2. Se os testes passarem, faça o build da imagem Docker.
> 3. (Opcional) Explique como usar GitHub Secrets para armazenar senhas do Docker Hub."

**Por que:**
Este é o ápice do MLOps: o "Loop de Feedback". O desenvolvedor apenas envia o código, e o robô cuida de testar, treinar e preparar a entrega.
