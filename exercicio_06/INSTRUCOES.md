# Instruções: O Curador de Moda — Fashion MNIST Classifier

## Pré-requisitos

- Python 3.10+ instalado
- Git (opcional)

---

## Passo 1: Criar e Ativar o Ambiente Virtual

```bash
# Dentro da pasta exercicio_06/
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

---

## Passo 2: Instalar Dependências

```bash
pip install -r requirements.txt
```

> **Atenção**: O `tensorflow` (~500MB) é necessário apenas para treino.
> A API em produção (e via Docker) não precisa dele.

---

## Passo 3: Treinar o Modelo

```bash
python train/train.py
```

**O que acontece:**
1. O Fashion MNIST é baixado (~30MB, armazenado em `~/.keras/`)
2. O MLPClassifier é treinado (~2-5 minutos, sem GPU)
3. O artefato é salvo em `model/fashion_classifier.joblib`

**Saída esperada:**
```
Baixando Fashion MNIST via tensorflow.keras...
  Imagens de treino: (60000, 28, 28)  |  Teste: (10000, 28, 28)
Iteration 1, loss = ...
...
Acurácia no conjunto de teste: 0.8790 (87.9%)
Modelo salvo em: .../model/fashion_classifier.joblib
```

---

## Passo 4: Iniciar a API

```bash
uvicorn app.main:app --reload
```

Acesse a documentação interativa: **http://localhost:8000/docs**

---

## Passo 5: Testar a API

### Via Swagger UI (navegador)
Acesse `http://localhost:8000/docs` → endpoint `/predict/upload` → "Try it out" → selecione uma imagem.

### Via curl (upload de arquivo)
```bash
curl -X POST http://localhost:8000/predict/upload \
     -F "file=@foto_camiseta.jpg"
```

### Via curl (array JSON)
```bash
curl -X POST http://localhost:8000/predict/array \
     -H "Content-Type: application/json" \
     -d '{"pixels": [128.0, 130.0, ...]}'  # 784 valores
```

### Verificar saúde
```bash
curl http://localhost:8000/health
# {"status":"ok","model_loaded":true,"version":"1.0.0"}
```

---

## Passo 6: Executar os Testes

```bash
pytest tests/ -v
```

---

## Passo 7: Interface Visual com Streamlit

Com a API rodando (`uvicorn app.main:app`), em outro terminal:

```bash
streamlit run streamlit_app.py
```

Acesse: **http://localhost:8501**

---

## Passo 8: Executar com Docker (Opcional)

### Pré-requisito
Ter o Docker Desktop instalado e em execução.

### Build da imagem
```bash
# Execute dentro da pasta exercicio_06/
docker build -t fashion-api .
```

### Executar o container
```bash
docker run -p 8000:8000 fashion-api
```

A API estará disponível em `http://localhost:8000/docs`.

> **Importante**: O modelo (`model/fashion_classifier.joblib`) deve estar presente
> antes do `docker build`, pois é copiado para dentro da imagem.

### Parar o container
```bash
# Listar containers em execução
docker ps

# Parar pelo ID
docker stop <container_id>
```

---

## Resolução de Problemas

| Problema | Causa | Solução |
|----------|-------|---------|
| `FileNotFoundError: Modelo não encontrado` | Modelo não treinado | Execute `python train/train.py` |
| `422 Unprocessable Entity` no upload | `python-multipart` não instalado | `pip install python-multipart` |
| `415 Unsupported Media Type` | Formato de imagem não suportado | Use JPEG, PNG, WebP ou BMP |
| `ModuleNotFoundError: tensorflow` | tensorflow não instalado | `pip install tensorflow` (apenas para treino) |
| Imagem classificada errada | Imagem muito diferente do dataset | Fashion MNIST usa fundo branco/cinza, peça centralizada |
