# =============================================================================
# ETAPA 1 — Builder: instala dependências em camada separada
# =============================================================================
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# =============================================================================
# ETAPA 2 — Runtime: imagem final enxuta
# =============================================================================
FROM python:3.11-slim

WORKDIR /app

# Copia pacotes instalados do builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copia o código da aplicação
COPY app/ ./app/
COPY models/ ./models/

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

# IMPORTANTE: o modelo já deve estar em models/ antes do build.
# Execute 'python src/train.py' localmente primeiro.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
