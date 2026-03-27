# Avaliação de Compra de Carros (MLOps — Linter)

Este projeto demonstra como automatizar a qualidade do código usando **GitHub Actions** e **Flake8 (Linter)**.

O objetivo principal é entender a importância de um código limpo e padronizado em ambientes de Machine Learning, onde a manutenção por equipes multidisciplinares é comum.

Para detalhes teóricos, consulte o [Guia de Teoria Aplicada](TEORIA.md) e para instruções de uso, veja o [Guia de Instruções](INSTRUCOES.md).

---

## 🛠️ Tecnologias

- **Dataset:** UCI Car Evaluation (via `ucimlrepo`).
- **Modelagem:** Scikit-Learn (RandomForest).
- **API:** FastAPI.
- **QA:** Flake8 + GitHub Actions.

---

## 🎯 Conceito MLOps: Linting

O **Linting** é o processo de analisar o código em busca de erros de estilo e bugs em potencial. Em MLOps, ele garante que:
- O código de pré-processamento seja legível.
- Não existam variáveis "mortas" ou imports inúteis que poluem o ambiente de produção.
- O padrão de escrita (PEP 8) seja uniforme entre todos os desenvolvedores.
