# Cadeia de Prompts — Eficiência Energética (Exercicio 02)

Esta sequência foca em um modelo de regressão com múltiplas saídas, usando dados acadêmicos externos.

---

## 1. Fonte de Dados e Estrutura
**Prompt:**
> "Quero criar uma API que preveja o consumo de energia de edifícios. Use o dataset 'Energy Efficiency' da UCI Machine Learning Repository (ID 242) via biblioteca `ucimlrepo`. 
> 
> Me ajude com o `requirements.txt` (FastAPI, Uvicorn, Scikit-Learn, Joblib, Pandas, ucimlrepo) e use uma das estruturas abaixo para o projeto:
>
> **Opção A (Hierarquia Clássica):**
> - `src/api/`: Pasta para o código da API FastAPI.
> - `src/training/`: Pasta para o script de treinamento.
> - `models/`: Pasta para o modelo serializado.
>
> **Opção B (Estrutura Minimalista):**
> - `main.py`: Código da API.
> - `training.py`: Código de treinamento.
> - `model_storage/`: Pasta para os arquivos `.joblib`."

**Por que:** 
Diferenciar as estruturas permite que a IA escolha a mais adequada para o tamanho do projeto, mantendo a organização de onde o modelo será armazenado.

---

## 2. Treinamento com Múltiplas Saídas
**Prompt:**
> "Desenvolva o script de treinamento (seguindo a estrutura escolhida). O script deve baixar o dataset via `ucimlrepo`, treinar um `RandomForestRegressor` para prever 'Heating Load' e 'Cooling Load' simultaneamente e salvar o modelo em `modelo_energia.joblib`."

**Por que:**
Regressão multi-saída é comum em problemas de engenharia. Especificar o download via biblioteca garante que o script seja executável em qualquer lugar que tenha internet.

---

## 3. Schemas e Tipagem
**Prompt:**
> "Defina os schemas no Pydantic. A entrada deve aceitar as 8 características arquitetônicas (área, altura, orientação, etc.) como floats. A saída deve ser um objeto JSON contendo as predições para carga de aquecimento e carga de resfriamento."

**Por que:**
Contratos de dados claros evitam confusão na integração entre o modelo matemático e a interface de resposta do usuário.

---

## 4. API com FastAPI
**Prompt:**
> "Crie a API FastAPI. Ao subir, ela deve carregar o modelo e ter um endpoint POST `/predict` que retorne as cargas térmicas estimadas. Adicione documentação descritiva para cada campo de entrada no Swagger UI."

**Por que:**
Documentar os campos diretamente no código ajuda quem vai consumir a API a entender o que cada característica física (como 'glazing_area') representa.

---

## 5. Validação Numérica
**Prompt:**
> "Escreva um teste simples em Pytest que simule uma chamada à API e verifique se as duas respostas numéricas são maiores que zero e do tipo float."

**Por que:**
Para regressões, o teste de "senso comum" (como garantir que o consumo de energia não seja negativo) é a primeira linha de defesa contra bugs no modelo.
