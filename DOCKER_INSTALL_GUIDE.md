# Guia de Instalação: Docker Desktop + WSL2 (via CMD)

Este guia descreve o processo de preparação do Windows para rodar containers Docker utilizando o backend do **WSL2**, que oferece performance superior e compatibilidade total com o ecossistema Linux.

---

## 1. Pré-requisitos
*   Windows 10 (versão 2004 ou superior) ou Windows 11.
*   Acesso de **Administrador**.

---

## 2. Passo a Passo (Prompt de Comando - CMD)

Abra o **Prompt de Comando (CMD)** como **Administrador** e execute os passos abaixo:

### Passo 2.1: Habilitar o Recurso de WSL
```cmd
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

### Passo 2.2: Habilitar o Recurso de Plataforma de Máquina Virtual
```cmd
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

### Passo 2.3: Definir WSL 2 como Versão Padrão
Após a execução dos comandos acima, **reinicie o computador** e execute:
```cmd
wsl --set-default-version 2
```

### Passo 2.4: Instalar uma Distribuição Linux (Opcional, mas recomendado)
Para testar o ambiente Linux independente do Docker:
```cmd
wsl --install -d Ubuntu
```

---

## 3. Instalação do Docker Desktop

1.  Baixe o instalador oficial: [Docker Desktop for Windows](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe).
2.  Execute o instalador.
3.  **Importante:** Na tela de configuração, certifique-se de que a opção **"Use the WSL 2 based engine"** está marcada.
4.  Após a instalação, encerre a sessão do Windows (Log out) ou reinicie para aplicar as mudanças de grupo de usuário.

---

## 4. Verificação da Instalação

Abra um novo CMD (não precisa ser admin) e verifique as versões:

### Checar versão do Docker
```cmd
docker --version
```

### Checar se o motor de containers está ativo
```cmd
docker info
```

### Rodar um container de teste
```cmd
docker run hello-world
```

### Verificar o status do WSL
```cmd
wsl --list --verbose
```
*Deverá aparecer uma instância chamada `docker-desktop` e `docker-desktop-data` com o status "Running" e versão 2.*

---

## 5. Dicas de Performance (MLOps)
Se você estiver trabalhando com datasets grandes (como nos exercícios de Diamond Price ou Fashion MNIST):
*   Sempre coloque os arquivos do projeto dentro do sistema de arquivos do WSL (ex: `\\wsl$\Ubuntu\home\usuario\projeto`) em vez de acessar `/mnt/c/`. O acesso a arquivos entre Windows e Linux via Docker é significativamente mais rápido dentro do sistema de arquivos nativo do Linux.
