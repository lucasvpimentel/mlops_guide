# Instruções — Previsão de Diamantes (Docker)

Este exercício foca na conteinerização. Siga os passos abaixo para rodar:

---

## 🚀 Como Executar

**1. Treinar o modelo localmente:**
*(Certifique-se de ter as dependências instaladas: `pip install -r requirements.txt`)*
```bash
python train/train.py
```

**2. Criar a Imagem Docker:**
```bash
docker build -t diamond-api .
```

**3. Rodar o Container:**
```bash
docker run -p 8000:8000 diamond-api
```
A API estará disponível em `http://localhost:8000/docs`.

---

## 🎯 Por que Docker?

O objetivo aqui é garantir a **portabilidade**. O Docker permite que o projeto rode em qualquer máquina sem precisar configurar o Python localmente.
