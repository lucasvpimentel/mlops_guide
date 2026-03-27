# Teoria: O Curador de Moda — Visão Computacional e Serialização de Imagens

## 1. O Problema: Dados Além de JSON

Nos exercícios anteriores, todos os dados de entrada eram números e textos simples,
enviados como JSON. Mas e quando o dado de entrada é uma **imagem**?

Uma imagem JPEG ou PNG é um arquivo binário. Ela não pode ser enviada diretamente
como JSON. Precisamos de um mecanismo diferente: o **upload de arquivo**.

```
Exercícios anteriores: { "feature1": 1.5, "feature2": "A" }   → JSON simples
Este exercício:         arquivo.jpg (binário, ~50KB)            → multipart/form-data
```

---

## 2. Como o FastAPI Lida com Upload de Arquivos

O FastAPI usa o padrão HTTP `multipart/form-data` para receber arquivos:

```python
from fastapi import UploadFile, File

@app.post("/predict/upload")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()  # Lê o conteúdo binário
```

**Dependência obrigatória**: `python-multipart` deve estar instalado.
Sem ele, o FastAPI retorna erro 422 ao tentar receber um arquivo.

---

## 3. O Pipeline de Pré-processamento de Imagens

O modelo não "entende" imagens — ele entende **arrays numéricos**.
O nosso trabalho é converter a imagem nesse array de forma consistente.

```
Arquivo JPEG
    ↓ io.BytesIO(image_bytes)
PIL.Image
    ↓ .convert("L")
Imagem em escala de cinza (1 canal)
    ↓ .resize((28, 28))
Imagem 28×28 pixels
    ↓ np.array(..., dtype=np.float32)
Array shape (28, 28), valores 0-255
    ↓ / 255.0
Array shape (28, 28), valores 0.0-1.0
    ↓ .flatten().reshape(1, -1)
Array shape (1, 784) ← pronto para o modelo
```

---

## 4. A Regra de Ouro: Simetria Treino-Serving

**O pré-processamento no serving DEVE ser idêntico ao do treino.**

| Etapa | Treino (`train.py`) | Serving (`model.py`) |
|-------|--------------------|-----------------------|
| Formato | Array NumPy bruto do Keras | Bytes de arquivo de imagem |
| Escala de cinza | Já é grayscale | `image.convert("L")` |
| Redimensionar | Já é 28×28 | `image.resize((28, 28))` |
| Normalizar | `/ 255.0` | `/ 255.0` |
| Achatar | `.reshape(-1, 784)` | `.flatten().reshape(1, -1)` |

Se você esquecer o `/255.0` no serving, o modelo receberá valores em [0, 255]
em vez de [0, 1] — e as predições serão completamente erradas.
Esse problema é chamado de **Training-Serving Skew**.

---

## 5. Fashion MNIST: O Dataset

O Fashion MNIST foi criado pela Zalando Research como substituto ao MNIST clássico
(dígitos manuscritos). É mais desafiador e representa um problema real de negócio.

| Característica | Valor |
|----------------|-------|
| Imagens de treino | 60.000 |
| Imagens de teste | 10.000 |
| Tamanho de cada imagem | 28×28 pixels |
| Canais de cor | 1 (grayscale) |
| Número de classes | 10 |
| Acurácia baseline (MLP) | ~87-88% |

**As 10 classes:**
0. Camiseta/Top  1. Calça  2. Pullover  3. Vestido  4. Casaco
5. Sandália  6. Camisa  7. Tênis  8. Bolsa  9. Bota

---

## 6. Dois Modos de Input: Upload vs Array JSON

A API oferece dois endpoints de predição para cobrir casos de uso diferentes:

| Endpoint | Entrada | Caso de uso |
|----------|---------|-------------|
| `POST /predict/upload` | Arquivo de imagem (JPEG/PNG) | Usuário final via navegador ou app |
| `POST /predict/array` | JSON com 784 floats | Scripts, notebooks, integração entre sistemas |

O endpoint `/predict/array` é especialmente útil para testes automatizados,
pois não requer criar um arquivo físico de imagem.

---

## 7. Streamlit: A Camada de Demonstração

O Streamlit é um framework Python para criar interfaces web interativas com poucas linhas.
Neste projeto, ele serve como **cliente visual** para a API FastAPI.

**Separação de responsabilidades:**
```
FastAPI (porta 8000)    → Lógica de ML, validação, inferência
Streamlit (porta 8501)  → Interface do usuário, visualização
```

Essa separação é uma boa prática de arquitetura: a API pode ser usada por qualquer
cliente (Streamlit, React, mobile app, outro serviço) sem modificação.

---

## 8. Referências

### Técnicas e Bibliográficas
*   **Streamlit:** Streamlit Inc. (2019). *Streamlit: The fastest way to build and share data apps*. [streamlit.io](https://streamlit.io/)
*   **Pillow (PIL):** Clark, A. (2010). *Pillow: The friendly PIL fork*. [python-pillow.org](https://python-pillow.org/)
*   **Artificial Neural Networks:** Haykin, S. (2009). *Neural Networks and Learning Machines*. Pearson.

### Dataset
*   **Fashion MNIST:** Xiao, H., Rasul, K., & Vollgraf, R. (2017). *Fashion-MNIST: a Novel Image Dataset for Benchmarking Machine Learning Algorithms*. arXiv:1708.07747. [github.com/zalandoresearch/fashion-mnist](https://github.com/zalandoresearch/fashion-mnist).
