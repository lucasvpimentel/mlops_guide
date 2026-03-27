# 🐳 Guia de Docker — Teoria e Prática MLOps

Docker é uma plataforma que permite automatizar o deploy de aplicações dentro de **containers** de software. No mundo de MLOps, o Docker é a ferramenta que resolve o problema do "funciona na minha máquina".

---

## 1. O que é um Container? 📦

Um container é uma unidade de software que empacota o código e todas as suas dependências (bibliotecas, configurações, runtime) para que a aplicação rode de forma rápida e confiável em qualquer ambiente.

### Diferença: Máquina Virtual vs. Container

| Característica | Máquina Virtual (VM) | Container (Docker) |
| :--- | :--- | :--- |
| **Isolamento** | Nível de Hardware (Hypervisor) | Nível de Processo (Kernel do OS) |
| **Tamanho** | Gigabytes (inclui um OS inteiro) | Megabytes (apenas a aplicação e libs) |
| **Velocidade** | Minutos para subir | Segundos para subir |

---

## 2. Anatomia do Docker (Visualização) 🖼️

### O Ciclo de Vida: Build, Ship, Run

```text
  [ Dockerfile ] ----> [ Imagem ] ----> [ Container ]
       (Receita)        (Fotografia)     (Execução)
```

---

## 3. Comandos de Ouro 🎖️

```bash
# Constrói uma imagem
docker build -t meu-projeto .

# Roda um container
docker run -p 8000:8000 meu-projeto
```
