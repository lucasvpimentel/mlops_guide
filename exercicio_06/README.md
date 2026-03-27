# Fashion MNIST Classifier (Exercicio 06)

Este projeto demonstra a classificação de imagens do dataset **Fashion MNIST** utilizando um modelo MLP (Multi-Layer Perceptron).

## 🚀 Como Rodar

### 💻 Localmente
1. Instale as dependências: `pip install -r requirements.txt`
2. Treine o modelo: `python train/train.py`
   * O script baixa o dataset via **OpenML** automaticamente (sem necessidade de TensorFlow).
3. Inicie a API: `uvicorn app.main:app --reload`
4. Inicie o Streamlit: `streamlit run streamlit_app.py`

### 🐳 Com Docker
1. Treine o modelo localmente: `python train/train.py`
2. Construa a imagem: `docker build -t fashion-api .`
3. Rode o container: `docker run -p 8000:8000 fashion-api`

Acesse a documentação da API em `http://localhost:8000/docs`.

## 🛠️ Detalhes Técnicos
- **Dataset**: Fashion MNIST (70k imagens 28x28 grayscale).
- **Modelo**: `MLPClassifier` (Scikit-Learn).
- **Treinamento**: O download e preparação dos dados agora são feitos via `sklearn.datasets.fetch_openml`, removendo a dependência pesada do TensorFlow para o ambiente de treinamento e execução.
- **Frontend**: Aplicação interativa com **Streamlit** para upload e classificação de imagens.

