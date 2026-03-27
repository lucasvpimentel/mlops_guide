# ---------------------------------------------------------------------------
# Imagem base: Python 3.12 slim (Debian mínimo, sem compiladores desnecessários)
# Motivo: menor superfície de ataque, pull mais rápido em CI/CD
# ---------------------------------------------------------------------------
FROM python:3.12-slim

# Variáveis de ambiente para comportamento determinístico do Python dentro do container
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Diretório de trabalho dentro do container
WORKDIR /app

# ---------------------------------------------------------------------------
# 1. Instalar dependências ANTES de copiar o código-fonte.
# Motivo: o Docker cacheia essa camada. Se só o código mudar (não o requirements),
# o pip install não é re-executado — builds muito mais rápidos.
# ---------------------------------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir --only-binary :all: -r requirements.txt

# ---------------------------------------------------------------------------
# 2. Copiar o código-fonte e o artefato treinado.
# model.joblib DEVE existir antes do 'docker build' (gerado por src/train.py).
# O CI/CD garante essa ordem: treinar → testar → buildar imagem.
# ---------------------------------------------------------------------------
COPY src/ ./src/
COPY app/ ./app/
COPY model.joblib .

# Porta exposta (documentação — o 'docker run -p' ainda é necessário)
EXPOSE 8000

# ---------------------------------------------------------------------------
# Comando padrão: iniciar o servidor uvicorn
# --host 0.0.0.0 → aceita conexões externas ao container (não só localhost)
# --workers 1    → adequado para containers stateless em orquestradores
# ---------------------------------------------------------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
