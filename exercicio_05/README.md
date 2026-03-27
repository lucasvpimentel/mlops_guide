# Avaliação de Compra de Carros (MLOps — Linter)

Este projeto demonstra como automatizar a qualidade do código usando **GitHub Actions** e **Flake8 (Linter)**.

O objetivo principal é entender a importância de um código limpo e padronizado em ambientes de Machine Learning, onde a manutenção por equipes multidisciplinares é comum.

Para detalhes teóricos, consulte o [Guia de Teoria Aplicada](TEORIA.md) e para instruções de uso, veja o [Guia de Instruções](INSTRUCOES.md).

---

## 🛠️ Tecnologias

- **Dataset:** UCI Car Evaluation (via `ucimlrepo`).
- **Modelagem:** Scikit-Learn (RandomForest).
- **API:** FastAPI.
- **QA:** Flake8 + GitHub Actions.

## 🚀 Como Rodar

### 💻 Localmente
1. Instale as dependências: `pip install -r requirements.txt`
2. Treine o modelo: `python src/train.py`
3. Inicie a API: `uvicorn app.main:app --reload`

### 🐳 Com Docker
1. Treine o modelo localmente: `python src/train.py`
2. Construa a imagem: `docker build -t car-api .`
3. Rode o container: `docker run -p 8000:8000 car-api`

Acesse a documentação em `http://localhost:8000/docs`.
