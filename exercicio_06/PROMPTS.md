# Cadeia de Prompts — O Curador de Moda (Exercicio 06)

Este projeto foca no processamento de imagens, redes neurais simples (MLP) e na criação de uma interface visual com Streamlit.

---

## 1. Fonte de Dados e Estrutura de Visão
**Prompt:**
> "Quero criar um sistema de classificação de roupas usando o dataset 'Fashion MNIST' (Zalando Research). Os dados devem ser carregados via `keras.datasets.fashion_mnist`. 
> 
> Me ajude com o `requirements.txt` (FastAPI, Uvicorn, Scikit-Learn, Pandas, Joblib, Pytest, Pillow, Streamlit, python-multipart) e escolha uma destas estruturas:
>
> **Opção A (Profissional):**
> - `app/`: Contém `main.py`, `schemas.py`, `model.py` (inferência).
> - `train/`: Contém `train.py` (treino do MLP).
> - `model/`: Pasta para o arquivo `.joblib`.
> - `streamlit_app.py`: Interface visual fora da pasta app.
>
> **Opção B (Minimalista):**
> - `api.py`: Código da API.
> - `trainer.py`: Código de treinamento.
> - `interface.py`: Código do Streamlit.
> - `models/`: Pasta para o modelo."

**Por que:** 
Diferente dos exercícios anteriores, aqui precisamos da biblioteca `Pillow` para manipular imagens e `python-multipart` para que o FastAPI consiga receber uploads de arquivos.

---

## 2. Treino de Rede Neural (MLP)
**Prompt:**
> "Escreva o script `train/train.py`. Ele deve carregar o Fashion MNIST do Keras, normalizar as imagens (dividir por 255.0), achatar os arrays (de 28x28 para 784) e treinar um `MLPClassifier` do Scikit-Learn. Salve o modelo treinado em `model/fashion_model.joblib`."

**Por que:**
O `MLPClassifier` é uma rede neural simples (Multi-Layer Perceptron). Treiná-lo com dados normalizados entre 0 e 1 é fundamental para a convergência do algoritmo.

---

## 3. Lógica de Processamento de Imagem
**Prompt:**
> "Crie em `app/model.py` uma função que receba os bytes de uma imagem enviada pelo usuário, converta para escala de cinza, redimensione para 28x28 pixels usando a biblioteca `Pillow`, normalize para o intervalo [0, 1] e retorne a predição do modelo."

**Por que:**
Esta é a parte mais crítica: a "Simetria". Se a imagem do usuário não for redimensionada e normalizada exatamente como os dados de treino, o modelo não conseguirá reconhecer a peça de roupa.

---

## 4. API com Upload de Arquivos
**Prompt:**
> "Desenvolva a API FastAPI em `app/main.py`. Crie um endpoint POST `/predict/upload` que aceite um `UploadFile` (imagem) e um endpoint POST `/predict/array` que aceite um JSON com 784 floats (para integração). Garanta que o modelo seja carregado apenas uma vez no startup."

**Por que:**
Oferecer dois tipos de entrada (Arquivo vs. JSON) torna a API versátil: o upload é ótimo para humanos, e o array JSON é ideal para outros sistemas ou scripts de teste.

---

## 5. Interface Visual (Streamlit)
**Prompt:**
> "Crie um aplicativo Streamlit em `streamlit_app.py`. Ele deve permitir que o usuário faça o upload de uma imagem (.jpg, .png), mostre a imagem na tela e chame a API FastAPI para exibir a categoria da roupa (ex: Camiseta, Bota, Bolsa) e a confiança da predição."

**Por que:**
O Streamlit permite criar um "protótipo vivo". Ver o modelo funcionando visualmente com fotos reais é a melhor forma de validar a experiência do usuário (UX) em projetos de IA.

---

## 6. Docker Multi-Processo
**Prompt:**
> "Crie um `Dockerfile` que instale todas as dependências e rode tanto a API (porta 8000) quanto o Streamlit (porta 8501). Explique como o Docker ajuda a manter a interface e o cérebro (modelo) unidos no mesmo ambiente."

**Por que:**
Conteinerizar a stack completa (API + Front) garante que qualquer pessoa possa testar a solução visual completa com apenas um comando `docker run`.
