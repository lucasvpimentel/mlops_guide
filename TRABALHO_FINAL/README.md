# Bank Marketing Subscription Predictor 🚀

Este projeto é uma solução completa de MLOps para prever se um cliente de uma instituição bancária irá subscrever a um depósito a prazo (investimento), com base em dados de campanhas de marketing direto.

## 🏦 Cenário de Negócio
A conversão de vendas em depósitos a prazo é crucial para bancos aumentarem sua base de ativos. Utilizando o dataset **Bank Marketing (UCI ID: 222)**, este projeto permite que a equipe de marketing foque seus esforços nos clientes com maior probabilidade de conversão, otimizando custos e aumentando a eficiência das chamadas telefônicas.

## 🛠️ Stack Tecnológica
- **Python 3.9+**
- **FastAPI**: Servidor web de alta performance.
- **Scikit-Learn**: Treinamento do modelo RandomForest.
- **UCIMLRepo**: Integração direta com o repositório UCI.
- **Joblib**: Para serialização do modelo.
- **Docker**: Containerização para deploy consistente.

## 📂 Estrutura do Projeto
```text
bank_marketing_pro/
├── app/
│   ├── main.py           # Servidor FastAPI com carregamento otimizado do modelo
│   └── schemas.py        # Validação de dados com Pydantic (idade > 18, etc)
├── models/               # Modelos e encoders serializados (.joblib)
├── scripts/
│   └── train_model.py    # Pipeline de treino (Extração, Transformação e Carga)
├── Dockerfile            # Imagem Docker baseada em python:3.9-slim
├── requirements.txt      # Dependências necessárias
└── README.md             # Esta documentação
```

## 🚀 Como Executar

### 1. Preparação do Ambiente
```bash
pip install -r requirements.txt
```

### 2. Treinamento do Modelo
Execute o script para baixar os dados do UCI, processar e salvar o modelo na pasta `models/`:
```bash
python scripts/train_model.py
```

### 3. Rodando via Docker (Recomendado)
Construa e suba a API em segundos:
```bash
docker build -t bank-marketing-api .
docker run -p 8000:8000 bank-marketing-api
```

## 📩 Entrega do Trabalho
Para a avaliação, o aluno deve seguir as instruções abaixo:

1.  **Destinatário:** lucasvpimentel@gmail.com
2.  **Assunto:** `[Seu Nome Completo] - mlops`
3.  **Conteúdo:** Envie o link do repositório GitHub com a solução completa.
4.  **Data Limite:** **04 de abril de 2026**.

---
*Projeto desenvolvido para fins educacionais - MBA MLOps.*