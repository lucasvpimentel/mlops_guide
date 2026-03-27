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

---

## 4. Referências

### Técnicas e Bibliográficas
*   **Pytest:** Krekel, H. et al. (2004). *pytest: help0.5 framework for unit, functional and integration testing*. [pytest.org](https://pytest.org/)
*   **Test-Driven Development (TDD):** Beck, K. (2003). *Test-Driven Development: By Example*. Addison-Wesley Professional.
*   **Quality Assurance in ML:** Breck, E. et al. (2017). *The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction*. IEEE International Conference on Big Data.

### Dataset
*   **Heart Disease:** Detrano, R. et al. (1989). *International application of a new probability algorithm for the diagnosis of coronary artery disease*. American Journal of Cardiology. [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/45/heart+disease).
