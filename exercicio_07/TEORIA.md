# Teoria Aplicada — Guia Simples MLOps

Este documento explica os conceitos teóricos por trás do projeto de forma simples, mostrando onde cada um é aplicado no código. Para instruções de uso, veja o [README.md](README.md).

---

## 1. Naive Bayes (O Classificador Probabilístico)

### O que é?
Imagine que o modelo é um assistente que "conta" quais palavras aparecem mais em mensagens **Spam** (indesejadas) e quais aparecem mais em **Ham** (boas). 
* Se ele vê "Ganhou", "Prêmio" e "Grátis", ele nota que essas palavras são muito comuns em Spam.
* Ele é "Naive" (Ingênuo) porque assume que cada palavra é independente das outras, o que simplifica o cálculo sem perder muita precisão em textos.

### Onde está no código?
Está no arquivo `src/train.py`, na função `build_pipeline()`, usando o `MultinomialNB()`. É o "cérebro" que toma a decisão final.

---

## 2. TF-IDF (Dando Peso às Palavras)

### O que é?
Modelos de ML não leem texto, eles leem números. O TF-IDF transforma palavras em pesos:
* **Term Frequency (TF):** Se a palavra aparece muito em uma mensagem, ela ganha pontos.
* **Inverse Document Frequency (IDF):** Se a palavra aparece em *todas* as mensagens (como "o", "a", "de"), ela perde pontos por ser comum demais e não ajudar a distinguir Spam de Ham.
* **Resultado:** Palavras raras e específicas (ex: "Bitcoin", "Promoção") ganham pesos maiores.

### Onde está no código?
Também no `src/train.py`, dentro do `TfidfVectorizer()`. Ele prepara o texto antes de entregar para o Naive Bayes.

---

## 3. Funções Puras (O Segredo da Consistência)

### O que é?
Uma função é "pura" quando ela sempre dá o mesmo resultado para o mesmo texto, sem depender de nada externo (como a hora do dia ou um banco de dados).
* **Por que é vital?** Se a limpeza do texto mudar entre o dia do treino e o dia da predição na API, o modelo pode se confundir.

### Onde está no código?
No arquivo `src/preprocessing.py`, a função `clean_text()`. Ela é usada tanto no `train.py` quanto no `model_loader.py`. Como ela é pura, garantimos que o modelo sempre "falará a mesma língua".

---

## 4. FastAPI e Pydantic (A Porta de Entrada e o Segurança)

### O que são?
* **FastAPI:** É o motor que faz o servidor web rodar rápido.
* **Pydantic:** É o "segurança" da entrada. Ele verifica se o que o usuário enviou é realmente um texto e não algo que possa quebrar o sistema.

### Onde está no código?
No `app/main.py`. O `PredictRequest` define as regras do que a API aceita, e o FastAPI gera automaticamente a página de testes (`/docs`).

---

## 5. Docker (A "Caixa" Padronizada)

### O que é?
Docker coloca o código, as bibliotecas e o Python dentro de uma "caixa" (container). Isso evita o clássico problema: *"Na minha máquina funciona, mas no servidor não"*.

### Onde está no código?
No arquivo `Dockerfile`. Ele define que usaremos o Python 3.12, instala as dependências e copia o modelo treinado para dentro da caixa, pronta para rodar em qualquer lugar.

---

## 6. CI/CD (O Inspetor Automático)

### O que é?
CI (Integração Contínua) e CD (Entrega Contínua) são como uma esteira de produção automática:
1. Você envia o código para o GitHub.
2. Um robô treina o modelo, roda os testes e verifica se está tudo certo.
3. Se o teste passar, ele cria a imagem Docker e envia para a nuvem.

### Onde está no código?
No arquivo `.github/workflows/main.yml`. Ele garante que nenhum modelo "quebrado" ou código sem testes chegue ao usuário final.

---

## 7. Testes Unitários (A Garantia de Qualidade)

### O que são?
São pequenos códigos que testam partes específicas do sistema. Se alguém mudar a regra de limpeza de texto por acidente, o teste falha e avisa o erro.

### Onde está no código?
No diretório `tests/test_preprocess.py`. Eles verificam se a limpeza de texto remove pontuações, converte para minúsculas e lida com espaços corretamente.

---

## 8. Referências

### Técnicas e Bibliográficas
*   **Naive Bayes:** Rish, I. (2001). *An empirical study of the naive Bayes classifier*. IJCAI.
*   **TF-IDF:** Jones, K. S. (1972). *A statistical interpretation of term specificity and its application in retrieval*. Journal of Documentation.
*   **GitHub Actions:** GitHub Inc. (2018). *GitHub Actions: Automate your workflow from idea to production*. [github.com/features/actions](https://github.com/features/actions).

### Dataset
*   **SMS Spam Collection:** Almeida, T.A., Hidalgo, J.M.G., & Yamakami, A. (2011). *Contributions to the Study of SMS Spam Filtering: New Collection and Results*. Proceedings of the 2011 ACM Symposium on Document Engineering (DocEng'11). [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/228/sms+spam+collection).
