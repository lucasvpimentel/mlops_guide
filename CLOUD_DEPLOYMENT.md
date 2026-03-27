# Guia de Cloud Deployment para MLOps

Após desenvolver e testar suas APIs localmente com Docker, o próximo passo na jornada de MLOps é o **Deployment em Nuvem**. Este guia detalha as principais estratégias, provedores e modelos de infraestrutura para colocar modelos em produção.

---

## 1. Os "Três Gigantes" da Nuvem

Existem três provedores principais que dominam o mercado, oferecendo serviços integrados de Machine Learning:

*   **Google Cloud Platform (GCP):** Considerada a mais amigável para desenvolvedores de ML. O serviço **Vertex AI** é o carro-chefe, unificando todo o ciclo de vida.
*   **Amazon Web Services (AWS):** A mais robusta e com maior fatia de mercado. O **Amazon SageMaker** é a ferramenta padrão para treinamento e deploy em larga escala.
*   **Microsoft Azure:** Excelente integração para empresas que já utilizam o ecossistema Microsoft. O **Azure Machine Learning** oferece ótimas capacidades de MLOps e Low-Code.

---

## 2. Modelos de Deployment (Infraestrutura)

### 2.1 Máquinas Virtuais (IaaS - Infrastructure as a Service)
*   **Serviços:** AWS EC2, Google Compute Engine, Azure VMs.
*   **Como funciona:** Você aluga um "computador na nuvem" com SO (Linux/Windows). Você é responsável por instalar o Docker, configurar o firewall e gerenciar atualizações.
*   **Prós:** Controle total sobre o hardware e software.
*   **Contras:** Alta sobrecarga operacional (você gerencia o servidor).
*   **Uso:** Quando você precisa de configurações de kernel customizadas ou drivers de GPU muito específicos.

### 2.2 Containers e Orquestração (CaaS - Container as a Service)
*   **Serviços:** Amazon EKS, Google Kubernetes Engine (GKE), Azure Kubernetes Service (AKS).
*   **Como funciona:** Utiliza o **Kubernetes** para gerenciar múltiplos containers. Se uma instância da sua API de Pinguins cair, o Kubernetes sobe outra automaticamente.
*   **Prós:** Escalabilidade massiva e alta disponibilidade.
*   **Uso:** Aplicações complexas que exigem escalonamento automático (Auto-scaling) baseado no tráfego.

### 2.3 Serverless Containers (PaaS - Platform as a Service)
*   **Serviços:** **Google Cloud Run**, AWS Fargate.
*   **Como funciona:** Você fornece apenas a imagem Docker. A nuvem gerencia o servidor, a escalabilidade e o roteamento. Se ninguém usar a API, ela pode "escalar para zero" (você não paga nada).
*   **Prós:** Custo-benefício excelente para APIs, zero manutenção de servidor.
*   **Uso:** **Ideal para os exercícios deste curso.** Perfeito para APIs FastAPI que recebem requisições sob demanda.

---

## 3. Serviços Gerenciados de ML (End-to-End)

Para projetos profissionais, costuma-se usar plataformas que gerenciam o modelo além da infraestrutura HTTP:

1.  **Endpoints de Predição:** Você faz o upload do seu arquivo `.joblib` para o Vertex AI (GCP) ou SageMaker (AWS), e eles criam automaticamente uma URL segura com monitoramento de latência e erros.
2.  **Feature Stores:** Repositórios centrais para armazenar as variáveis (features) que o modelo usa, garantindo que o treino e a produção usem os mesmos dados.
3.  **Model Registry:** Um "catálogo" de versões do modelo (ex: v1, v2, v3), permitindo rollback imediato se uma versão nova apresentar problemas.

---

## 4. Comparativo de Estratégias

| Estratégia | Controle | Facilidade | Custo (Baixo Volume) | Recomendação |
| :--- | :--- | :--- | :--- | :--- |
| **VM (EC2/GCE)** | Máximo | Baixa | Fixo (Médio) | Ambientes Legados |
| **Cloud Run / Fargate** | Médio | Alta | Variável (Baixo) | **APIs Modernas / MVPs** |
| **Kubernetes (GKE/EKS)** | Alto | Baixa | Fixo (Alto) | Grandes Corporações |
| **Vertex AI / SageMaker** | Médio | Alta | Variável (Médio) | **Projetos de Data Science Profissionais** |

---

## 5. Próximos Passos (Integração Contínua)

O fluxo ideal de MLOps que conecta seu código a essas nuvens é:
1.  **Code:** Você commita no GitHub.
2.  **CI (GitHub Actions):** Roda o Flake8 e Pytest (como fizemos).
3.  **CD (Continuous Deployment):** Se os testes passarem, o GitHub Actions faz o build da imagem Docker e a envia automaticamente para o **Google Cloud Run** ou **AWS ECR**.

Isso garante que a versão que está rodando na nuvem é sempre a versão testada e aprovada do seu repositório.
