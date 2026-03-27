# Teoria — Docker e a Portabilidade de Modelos de ML

Este exercício foca no último elo da cadeia de entrega de um modelo de Machine Learning: a **Conteinerização**. O objetivo é garantir que o seu modelo rode da mesma forma no seu computador, no servidor de nuvem ou na máquina de um colega.

---

## 1. O Problema: "Funciona na Minha Máquina"

Em projetos de Machine Learning, a "máquina" não é apenas o sistema operacional. Ela inclui:
- A versão exata do Python.
- As versões das bibliotecas (Scikit-Learn, Pandas).
- Drivers e variáveis de ambiente.

---

## 2. A Solução: Docker

O Docker permite empacotar o código, o modelo treinado (`.joblib`), as bibliotecas (`requirements.txt`) e até o sistema operacional em uma unidade única chamada **Imagem**.

### Fluxo de Trabalho
1. **Build:** O Docker lê o `Dockerfile` e cria a imagem (o "computador congelado").
2. **Run:** O Docker cria um container (a instância rodando) a partir da imagem.

---

## 3. Por que o Modelo deve estar "Congelado"?

No MLOps, evitamos treinar o modelo dentro do Dockerfile. O ideal é treinar localmente (ou em um servidor de treino), validar o artefato `.joblib` e então copiá-lo para dentro do container. Isso garante que a imagem seja leve e que o modelo seja exatamente aquele que foi testado.

---

## 4. Referências

### Técnicas e Bibliográficas
*   **Docker:** Docker Inc. (2013). *Docker: Empowering App Development for Developers*. [docker.com](https://www.docker.com/)
*   **Containerization in ML:** Merkel, D. (2014). *Docker: lightweight linux containers for consistent development and deployment*. Linux Journal.
*   **12-Factor App:** Wiggins, A. (2011). *The Twelve-Factor App*. [12factor.net](https://12factor.net/) (Princípios de isolamento de dependências).

### Dataset
*   **Diamonds:** Wickham, H. (2016). *ggplot2: Elegant Graphics for Data Analysis*. Springer-Verlag New York. [Diamonds dataset documentation](https://ggplot2.tidyverse.org/reference/diamonds.html).
