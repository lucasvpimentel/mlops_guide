"""
Interface visual para o Fashion MNIST Classifier.

Esta aplicação Streamlit serve como cliente da API FastAPI.
Demonstra como separar a camada de UI da lógica de ML.

Para usar:
    1. Inicie a API: uvicorn app.main:app --reload
    2. Em outro terminal: streamlit run streamlit_app.py
    3. Acesse: http://localhost:8501
"""

import io

import numpy as np
import requests
import streamlit as st
from PIL import Image

# ---------------------------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="O Curador de Moda",
    page_icon="👗",
    layout="wide",
)

API_URL = "http://localhost:8000"

CLASSES = [
    "Camiseta/Top", "Calça", "Pullover", "Vestido", "Casaco",
    "Sandália", "Camisa", "Tênis", "Bolsa", "Bota",
]

CLASS_EMOJIS = {
    "Camiseta/Top": "👕",
    "Calça": "👖",
    "Pullover": "🧥",
    "Vestido": "👗",
    "Casaco": "🧣",
    "Sandália": "👡",
    "Camisa": "👔",
    "Tênis": "👟",
    "Bolsa": "👜",
    "Bota": "👢",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def check_api_health() -> bool:
    """Verifica se a API está disponível e o modelo carregado."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        data = response.json()
        return response.status_code == 200 and data.get("model_loaded", False)
    except Exception:
        return False


def predict_from_upload(image_bytes: bytes, filename: str = "image.png") -> dict:
    """Envia a imagem para a API e retorna o resultado da predição."""
    response = requests.post(
        f"{API_URL}/predict/upload",
        files={"file": (filename, image_bytes, "image/png")},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def image_to_bytes(image: Image.Image) -> bytes:
    """Converte PIL.Image para bytes PNG."""
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()


def show_preprocessed_preview(image: Image.Image) -> Image.Image:
    """Retorna a versão 28×28 grayscale da imagem (como o modelo vê)."""
    return image.convert("L").resize((28, 28))


# ---------------------------------------------------------------------------
# Interface principal
# ---------------------------------------------------------------------------


def main():
    # Cabeçalho
    st.title("👗 O Curador de Moda")
    st.markdown(
        "Classifique peças de roupa usando um modelo treinado no **Fashion MNIST** (Zalando)."
    )

    # Status da API
    api_ok = check_api_health()
    if api_ok:
        st.success("API conectada e modelo carregado.", icon="✅")
    else:
        st.error(
            "API não disponível. Inicie com: `uvicorn app.main:app --reload`",
            icon="🔴",
        )
        st.stop()

    st.divider()

    # ---------------------------------------------------------------------------
    # Seção de upload
    # ---------------------------------------------------------------------------
    st.subheader("Envie uma imagem de roupa")

    col_upload, col_example = st.columns([3, 1])

    with col_upload:
        uploaded_file = st.file_uploader(
            "Escolha uma imagem (JPEG, PNG, WebP)",
            type=["jpg", "jpeg", "png", "webp", "bmp"],
        )

    with col_example:
        st.markdown("**Ou use um exemplo:**")
        if st.button("Gerar exemplo aleatório", use_container_width=True):
            # Gera imagem sintética aleatória (apenas para demonstração)
            random_pixels = np.random.randint(0, 256, (28, 28), dtype=np.uint8)
            example_img = Image.fromarray(random_pixels, mode="L").resize((200, 200))
            buf = io.BytesIO()
            example_img.save(buf, format="PNG")
            st.session_state["example_bytes"] = buf.getvalue()
            st.info("Imagem aleatória gerada (resultado pode não ser preciso).")

    # Determina qual imagem usar
    image_bytes = None
    source_image = None

    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        source_image = Image.open(io.BytesIO(image_bytes))
    elif "example_bytes" in st.session_state:
        image_bytes = st.session_state["example_bytes"]
        source_image = Image.open(io.BytesIO(image_bytes))

    # ---------------------------------------------------------------------------
    # Resultado
    # ---------------------------------------------------------------------------
    if image_bytes is not None and source_image is not None:
        st.divider()

        col_img, col_result = st.columns([1, 2])

        with col_img:
            st.markdown("**Imagem enviada**")
            st.image(source_image.resize((200, 200)), width=200)

            st.markdown("**Como o modelo vê** (28×28 grayscale)")
            preview = show_preprocessed_preview(source_image)
            # Ampliar para visualização
            preview_large = preview.resize((140, 140), Image.NEAREST)
            st.image(preview_large, width=140)

        with col_result:
            st.markdown("**Resultado da Classificação**")

            with st.spinner("Classificando..."):
                try:
                    result = predict_from_upload(image_bytes)
                except Exception as e:
                    st.error(f"Erro ao classificar: {e}")
                    st.stop()

            category = result["category"]
            emoji = CLASS_EMOJIS.get(category, "🏷️")
            confidence = result["confidence"]

            # Destaque principal
            st.markdown(f"## {emoji} {category}")
            st.progress(confidence, text=f"Confiança: {confidence * 100:.1f}%")

            st.markdown("---")
            st.markdown("**Distribuição de probabilidades:**")

            # Tabela de probabilidades
            probs = result["probabilities"]
            prob_data = {
                "Categoria": list(probs.keys()),
                "Probabilidade": [f"{v * 100:.1f}%" for v in probs.values()],
                "Barra": list(probs.values()),
            }

            # Gráfico de barras
            chart_data = {k: v for k, v in probs.items()}
            st.bar_chart(chart_data, height=300)

    # ---------------------------------------------------------------------------
    # Rodapé informativo
    # ---------------------------------------------------------------------------
    st.divider()
    with st.expander("Como funciona internamente?"):
        st.markdown("""
        1. **Você envia** uma imagem JPEG/PNG pelo navegador.
        2. **O Streamlit** lê os bytes e faz um `POST /predict/upload` para a API FastAPI.
        3. **A API** recebe os bytes, converte para grayscale 28×28, normaliza para [0,1] e passa ao modelo.
        4. **O modelo** (MLPClassifier) retorna probabilidades para as 10 classes.
        5. **A API** retorna o JSON com categoria, confiança e distribuição.
        6. **O Streamlit** exibe o resultado visualmente.

        ```
        Você → [Streamlit :8501] → POST /predict/upload → [FastAPI :8000] → MLPClassifier
                                                                                    ↓
        Você ← [Streamlit :8501] ← JSON {category, confidence} ← [FastAPI :8000] ←─┘
        ```
        """)


if __name__ == "__main__":
    main()
