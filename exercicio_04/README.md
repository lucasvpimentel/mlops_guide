# Heart Disease Diagnosis API (Exercicio 04)

Este exercício foca na **Qualidade de Software** aplicada ao MLOps. Utilizamos o dataset `Heart Disease` da UCI para classificar o risco cardíaco, com um rigoroso sistema de testes automatizados.

## 🎯 Foco MLOps: Testes Automatizados e Resiliência
Diferente dos exercícios anteriores que focaram em serialização e docker, aqui o objetivo é garantir que a aplicação seja **testável e confiável**.

### O que garantimos com este exercício:
- **Proteção do Modelo:** Nenhuma predição é feita se os dados de entrada forem biologicamente impossíveis (ex: idade > 150 anos).
- **Consistência de API:** Testes de integração garantem que os endpoints `/health`, `/info` e `/predict` funcionam conforme o contrato.
- **Automação:** Uso do `pytest` para validação rápida de regressões.

## 🚀 Como Rodar

### 💻 Localmente
1. Instale as dependências: `pip install -r requirements.txt`
2. Treine o modelo: `python train/train.py`
3. Inicie a API: `uvicorn app.main:app --reload`

### 🐳 Com Docker
1. Treine o modelo localmente: `python train/train.py`
2. Construa a imagem: `docker build -t heart-api .`
3. Rode o container: `docker run -p 8000:8000 heart-api`

Acesse a documentação em `http://localhost:8000/docs`.
