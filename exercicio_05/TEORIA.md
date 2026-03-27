# Teoria — Linting: O Código Limpo em MLOps

Em MLOps, o código do modelo é tão importante quanto os dados. Quando trabalhamos em equipe, garantir que todos sigam o mesmo padrão de escrita é vital para a manutenção do projeto.

---

## 1. O que é um Linter?

Um **Linter** é uma ferramenta que analisa o seu código em busca de erros de programação, bugs, erros de estilo e construções suspeitas. Ele funciona como um "corretor ortográfico" para código.

Neste exercício, usamos o **Flake8**, que verifica:
- **Erros de sintaxe:** Código que não vai rodar.
- **Estilo (PEP 8):** Indentações erradas, excesso de espaços em branco, etc.
- **Variáveis e Imports:** Avisa se você importou algo que não está usando (o que economiza memória).

---

## 2. Por que usar Linter em MLOps?

1.  **Redução de Erros Silenciosos:** Um import não utilizado ou uma variável sobrescrita acidentalmente pode causar comportamentos estranhos no modelo.
2.  **Facilidade de Revisão:** Código padronizado é mais fácil de ler para outro desenvolvedor.
3.  **Higiene de Produção:** Garante que o código que vai para o servidor é limpo e eficiente.

---

## 3. Integração Contínua (CI) e Qualidade

O GitHub Action que configuramos atua como um **"Portão de Qualidade"**.
- Se o desenvolvedor enviar um código "sujo", o Action falha.
- Isso impede que código de baixa qualidade chegue à branch principal, forçando boas práticas desde o início.

---

## 4. Como rodar localmente?

Antes de enviar seu código para o GitHub, você deve sempre rodar o linter localmente:
```bash
flake8 .
```
Se ele não retornar nada, seu código está "bonito" e pronto para o deploy!
