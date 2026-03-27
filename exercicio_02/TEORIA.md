# MLOps Avançado: Sommelier Digital — Serialização e Artefatos

Este exercício é um estudo de caso sobre o desacoplamento técnico entre o **ambiente de desenvolvimento (Training)** e o **ambiente de execução (Serving)**. No MLOps, este é um dos primeiros passos para a maturidade de nível 1, seja para prever a qualidade de um vinho ou o consumo de energia de um prédio.

## 1. O Conceito de Artefato de ML
Em software tradicional, o "artefato" costuma ser um binário (.exe), um JAR ou uma imagem Docker. Em Machine Learning, o artefato é o **estado congelado** de um algoritmo após ver dados. 
- Ele contém os pesos matemáticos (coeficientes, árvores, vetores).
- Ele contém o "conhecimento" extraído do dataset Energy Efficiency.

## 2. Por que Serializar? (A Muralha da Separação)
Se não serializássemos, a API teria que treinar o modelo toda vez que subisse. Isso seria catastrófico por três motivos:
1.  **Custo Computacional:** Treinar gasta CPU/GPU e tempo. Uma API deve subir em segundos, não minutos.
2.  **Não-Determinismo:** Se os dados mudarem na fonte, dois workers da mesma API poderiam treinar modelos diferentes, gerando predições inconsistentes para o mesmo usuário.
3.  **Ambientes Distintos:** O ambiente de treino muitas vezes precisa de bibliotecas de análise (seaborn, matplotlib, ucimlrepo) que **não devem** estar na imagem de produção para mantê-la leve e segura.

## 3. O Perigo do "Training-Serving Skew"
Este é o erro mais comum em ML: quando os dados são processados de um jeito no treino e de outro na API.
- **Exemplo:** Se no treino você normalizou a `surface_area_m2` dividindo por 1000, mas na API esqueceu de fazer isso, o modelo receberá um valor "gigante" e a predição será lixo.
- **A Solução (Pipelines):** Usamos o `sklearn.pipeline.Pipeline`. Ao salvar o pipeline, salvamos o `StandardScaler` **junto** com o regressor. O escalonador "lembra" da média e do desvio padrão do treino e os aplica na API de forma idêntica.

## 4. Validação Física e Deriva de Dados (Data Drift)
O uso de Pydantic com `ge` (greater or equal) e `le` (less or equal) no `schemas.py` não é apenas para evitar erros de código, é para garantir a **Consistência do Domínio**.
- O modelo de Gradient Boosting é péssimo em **extrapolação**. Se ele nunca viu um prédio com `overall_height_m` de 50 metros, ele vai inventar um número sem base estatística.
- Bloquear esses inputs na camada de API protege a integridade do sistema e evita que o modelo responda sobre cenários que ele desconhece.

## 5. Práticas Recomendadas Implementadas Aqui
- **Singleton Pattern:** O modelo é carregado uma única vez no startup (`lifespan`) e mantido em memória RAM.
- **Versão no Artefato:** O arquivo `.joblib` carrega sua própria versão, permitindo que a API informe ao usuário qual "cérebro" está gerando aquela resposta.
- **Saúde com Dependência:** O endpoint `/health` só retorna `model_loaded: true` se o artefato foi carregado com sucesso, permitindo que orquestradores (Kubernetes) saibam se o nó está pronto.
