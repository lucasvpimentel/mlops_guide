# Heart Disease Diagnosis API (Exercicio 04)

Este exercício foca na **Qualidade de Software** aplicada ao MLOps. Utilizamos o dataset `Heart Disease` da UCI para classificar o risco cardíaco, com um rigoroso sistema de testes automatizados.

## 🎯 Foco MLOps: Testes Automatizados e Resiliência
Diferente dos exercícios anteriores que focaram em serialização e docker, aqui o objetivo é garantir que a aplicação seja **testável e confiável**.

### O que garantimos com este exercício:
- **Proteção do Modelo:** Nenhuma predição é feita se os dados de entrada forem biologicamente impossíveis (ex: idade > 150 anos).
- **Consistência de API:** Testes de integração garantem que os endpoints `/health`, `/info` e `/predict` funcionam conforme o contrato.
- **Automação:** Uso do `pytest` para validação rápida de regressões.

## 🛠️ Tecnologias
- **FastAPI**
- **Pydantic** (Validação Biológica)
- **Pytest** (Suíte de Testes)
- **Scikit-Learn** (RandomForestClassifier)

Leia o arquivo [TEORIA.md](TEORIA.md) para entender como testes automatizados evitam o "Garbage In, Garbage Out" em produção.
