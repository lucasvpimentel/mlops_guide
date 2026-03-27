# Energy Efficiency MLOps Project (Exercicio 02)

Este repositório contém um projeto educacional de MLOps focado na **serialização de artefatos de modelo**. O objetivo é prever a carga de aquecimento (`Heating Load`) de edifícios com base em suas características construtivas, utilizando o dataset **UCI Energy Efficiency**.

## 🚀 Estrutura do Projeto

```text
exercicio_02/
├── app/                  # Código fonte da API FastAPI
│   ├── main.py           # Endpoints e ciclo de vida (startup/shutdown)
│   ├── schemas.py        # Contratos Pydantic com validação física
│   ├── model.py          # Lógica de inferência e singleton do modelo
│   └── config.py         # Configurações globais e paths
├── train/                # Scripts de Treinamento (Offline)
│   └── train.py          # Script que gera o artefato .joblib
├── model/                # Diretório que armazena os artefatos serializados
├── tests/                # Testes automatizados (pytest)
├── requirements.txt      # Dependências do projeto
├── Dockerfile            # ARQUIVO ILUSTRATIVO (Não é a fonte primária de execução)
├── TEORIA.md             # Conceitos técnicos de MLOps
└── INSTRUCOES.md         # Guia passo a passo de execução
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+**
- **FastAPI**: Servidor web assíncrono.
- **Scikit-Learn**: Para treinamento do `GradientBoostingRegressor`.
- **Pydantic**: Validação rigorosa de dados.
- **Joblib**: Serialização eficiente de objetos Python (artefatos).
- **ucimlrepo**: Acesso programático ao repositório UCI.

## 📈 Resumo Técnico

- **Algoritmo**: Gradient Boosting Regressor.
- **Pipeline**: O modelo inclui automaticamente o escalonamento de dados (`StandardScaler`) no artefato.
- **Validação**: Bloqueia entradas fora do range estatístico do treino (evitando erros de extrapolação).
- **Performance**: A inferência em memória é executada em milissegundos.

## 📖 Como começar?

Para entender a teoria por trás deste exercício, leia o arquivo [TEORIA.md](TEORIA.md). Para rodar o projeto localmente ou via Docker, siga as [INSTRUCOES.md](INSTRUCOES.md).
