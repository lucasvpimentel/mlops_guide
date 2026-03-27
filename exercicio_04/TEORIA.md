# Qualidade e Testes no Ciclo de MLOps

Em modelos de saúde (como diagnóstico cardíaco), a margem de erro deve ser minimizada não apenas no modelo estatístico, mas em toda a infraestrutura de software.

## 1. O Conceito de "Fail Fast" (Falhar Rápido)
A pior coisa que pode acontecer em uma API de ML é o modelo tentar prever algo baseado em dados impossíveis.
- **Cenário:** Um usuário envia acidentalmente `age=540`.
- **Sem Validação:** O modelo (que só viu idades de 29 a 77) tentaria fazer uma conta matemática e retornaria um "Risco: 20%", o que é clinicamente absurdo.
- **Com Validação (Pydantic + Pytest):** A API bloqueia a requisição instantaneamente com um erro `422`, protegendo o modelo de dados de baixa qualidade (Garbage In, Garbage Out).

## 2. Tipos de Testes Implementados
Neste exercício, focamos em dois pilares:
1.  **Testes Unitários de Schema (`test_schemas.py`):** Garantem que as regras de negócio biológicas (limites de pressão, colesterol, idade) estão codificadas corretamente no Pydantic.
2.  **Testes de Integração de API (`test_api.py`):** Garantem que os endpoints respondem corretamente aos códigos HTTP e que o modelo é carregado no startup sem falhas.

## 3. Por que usar Pytest?
- **Reprodutibilidade:** Garante que qualquer mudança futura no código (refatoração) não quebre as regras de validação existentes.
- **Documentação Viva:** Os testes servem como um exemplo de como a API deve se comportar em casos de sucesso e erro.
- **Confiança no Deploy:** Em um pipeline real de CI/CD, os testes rodam antes de qualquer deploy. Se um teste falha (ex: alguém removeu a trava de idade), o deploy é cancelado.
