# Previsão de Preço de Diamantes (Docker Básico)

Este projeto demonstra como conteinerizar uma aplicação de Machine Learning usando **Docker**.

Para detalhes teóricos, consulte o [Guia de Teoria Aplicada](TEORIA.md) e para instruções de uso, veja o [Guia de Instruções](INSTRUCOES.md).

## 🚀 Como Rodar

### 💻 Localmente
1. Instale as dependências: `pip install -r requirements.txt`
2. Treine o modelo: `python train/train.py`
3. Inicie a API: `uvicorn app.main:app --reload`

### 🐳 Com Docker
1. Treine o modelo localmente: `python train/train.py`
2. Construa a imagem: `docker build -t diamond-api .`
3. Rode o container: `docker run -p 8000:8000 diamond-api`

Acesse a documentação em `http://localhost:8000/docs`.
