# Guia de GitHub Actions — Automação MLOps

Este guia explica como o GitHub Actions automatiza o ciclo de vida deste projeto e como você pode construir suas próprias automações (Workflows). Para instruções gerais, veja o [README.md](README.md).

---

## 1. O que é o GitHub Actions?

O GitHub Actions é um motor de automação que executa tarefas baseadas em eventos (como um "push" de código). Ele funciona através de **Workflows** (fluxos de trabalho) escritos em arquivos YAML.

### Estrutura de Pastas
Para que o GitHub reconheça seus fluxos, eles **devem** estar nesta pasta específica:
```
.github/
└── workflows/
    └── main.yml   <-- Onde a mágica acontece
```

---

## 2. Anatomia de um Workflow

Para construir um workflow, você precisa entender quatro conceitos básicos:

1.  **Events (on):** O que dispara o robô? (Ex: `push`, `pull_request`).
2.  **Jobs:** O que deve ser feito? (Ex: `test`, `build`). Jobs rodam em paralelo por padrão.
3.  **Runner (runs-on):** Em qual sistema operacional o robô vai rodar? (Geralmente `ubuntu-latest`).
4.  **Steps:** A lista de comandos que o robô vai executar dentro de um Job.

---

## 3. Como funciona o nosso Pipeline (`main.yml`)

Nosso pipeline é dividido em duas grandes fases (Jobs):

### Fase 1: Testes e Treino (`job: test`)
O objetivo aqui é garantir que o código novo não quebrou nada.
*   **Checkout:** O robô "clona" seu código.
*   **Setup Python:** Ele instala a versão correta do Python.
*   **Train:** Ele executa `python -m src.train` para criar o `model.joblib`.
*   **Pytest:** Ele roda os testes. Se um teste falhar, o pipeline para e avisa você.
*   **Artifacts:** Como cada Job roda em uma máquina limpa, usamos `upload-artifact` para guardar o modelo treinado e passá-lo para a próxima fase.

### Fase 2: Docker e Entrega (`job: build-and-push`)
Só acontece se a Fase 1 passar com sucesso.
*   **Needs:** Usamos `needs: test` para dizer que este job depende do anterior.
*   **Secrets:** Para enviar a imagem ao Docker Hub, o robô precisa de uma senha. Usamos `secrets.DOCKERHUB_TOKEN` para que sua senha nunca apareça no código.
*   **Docker Build:** Ele cria a imagem e a envia para a nuvem.

---

## 4. O básico necessário para construir um do zero

Se você quiser criar um novo arquivo `.github/workflows/teste.yml`, aqui está o modelo mínimo:

```yaml
name: Meu Primeiro Robô

on: [push] # Roda sempre que houver um push

jobs:
  verificar-codigo:
    runs-on: ubuntu-latest
    steps:
      - name: Baixar codigo
        uses: actions/checkout@v4

      - name: Dizer Ola
        run: echo "O codigo foi baixado com sucesso!"
```

---

## 5. Como configurar os Segredos (Secrets)

Para que o envio ao Docker Hub funcione, você precisa cadastrar suas credenciais no GitHub:

1.  Vá no seu repositório no GitHub.
2.  Clique em **Settings** -> **Secrets and variables** -> **Actions**.
3.  Clique em **New repository secret**.
4.  Adicione:
    *   `DOCKERHUB_USERNAME`: Seu nome de usuário no Docker Hub.
    *   `DOCKERHUB_TOKEN`: Sua senha ou token do Docker Hub.

---

## 6. Dicas de Ouro

*   **Fail Fast:** Coloque os testes logo no início. Se houver erro, você economiza tempo de processamento.
*   **Cuidado com a Indentação:** Arquivos YAML são muito sensíveis a espaços. Use sempre 2 espaços para cada nível.
*   **Aba "Actions":** No seu repositório do GitHub, clique na aba **Actions** para ver o robô trabalhando em tempo real e ler os logs de erro caso algo falhe.
