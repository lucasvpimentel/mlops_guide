# 🌐 Guia de APIs REST Aplicadas a IA (MLOps)

Uma API (Application Programming Interface) é o "garçom" que leva o pedido do cliente (usuário) até a cozinha (modelo de Machine Learning) e traz a resposta (predição).

---

## 1. O Fluxo de uma Predição 🔄

```text
[ Cliente ] --(JSON: {carat: 0.5})--> [ FastAPI ] --(DataFrame)--> [ Modelo ML ]
                                                                       |
[ Cliente ] <--(JSON: {price: 1500})-- [ FastAPI ] <--(Predição: 1500)---+
```

---

## 2. Status Codes Principais 🚩

| Código | Significado |
| :--- | :--- |
| **200 OK** | Sucesso! |
| **422 Unprocessable** | Erro de Validação (dados inválidos). |
| **500 Error** | Erro do Servidor. |
