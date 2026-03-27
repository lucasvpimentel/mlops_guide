# #############################################################################
# DOCKERFILE ILUSTRATIVO - APENAS PARA FINS DIDÁTICOS
# #############################################################################
# ESTE ARQUIVO NÃO É A FONTE PRIMÁRIA DE EXECUÇÃO DESTE EXERCÍCIO.
# O objetivo deste Dockerfile é demonstrar como seria o empacotamento de uma
# aplicação de ML em um ambiente isolado. Para este curso, utilize a 
# execução via ambiente virtual (.venv) descrita no INSTRUCOES.md.
# #############################################################################

FROM python:3.11-slim

WORKDIR /app

# Instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte
COPY . .

# Nota: Em um cenário real, o modelo (.joblib) seria copiado para dentro 
# da imagem ou baixado de um Model Registry durante o build.
# Aqui, assume-se que você já rodou o train.py localmente.

EXPOSE 8000

# Comando para subir a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
