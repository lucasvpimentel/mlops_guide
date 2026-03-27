# ============================================================
# Dockerfile — Fashion MNIST Classifier API
# ============================================================
#
# CONCEITO: Por que usar Docker?
#
# Sem Docker: "Funciona na minha máquina" — o aluno precisa instalar
# Python, criar venv, instalar dependências na versão correta.
#
# Com Docker: Uma única imagem contém tudo. Qualquer pessoa roda com:
#   docker build -t fashion-api .
#   docker run -p 8000:8000 fashion-api
#
# A imagem é portável: funciona no Linux, Mac, Windows e em qualquer
# servidor de nuvem (AWS, Azure, GCP) sem modificação.
# ============================================================

# Estágio 1: Builder — instala dependências
# Separamos o build das deps do código para aproveitar o cache do Docker.
# Se só o código mudar, o Docker reutiliza a camada de dependências.
FROM python:3.11-slim AS builder

WORKDIR /app

# Instala dependências primeiro (camada cacheada pelo Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ============================================================
# Estágio 2: Runtime — imagem final enxuta
# ============================================================
FROM python:3.11-slim

WORKDIR /app

# Copia apenas os pacotes instalados (não o pip, build tools, etc.)
COPY --from=builder /usr/local/lib/python3.11/site-packages \
                    /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copia o código da aplicação e o artefato de modelo
COPY app/ ./app/
COPY model/ ./model/

# Variáveis de ambiente recomendadas para containers Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

# Inicia a API com uvicorn (sem --reload em produção)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
