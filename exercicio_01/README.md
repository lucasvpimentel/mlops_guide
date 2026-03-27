# Penguin Species Classifier (Exercicio 01)

Este projeto demonstra a criação de uma API de classificação de espécies de pinguins utilizando o dataset **Palmer Penguins**.

## 🚀 Como Rodar

### 💻 Localmente
1. Instale as dependências: `pip install -r requirements.txt`
2. Treine o modelo: `python train/train_model.py`
3. Inicie a API: `uvicorn app.main:app --reload`

### 🐳 Com Docker
1. Treine o modelo localmente: `python train/train_model.py`
2. Construa a imagem: `docker build -t penguin-api .`
3. Rode o container: `docker run -p 8000:8000 penguin-api`

Acesse a documentação em `http://localhost:8000/docs`.
