# Instruções de Execução — Exercício 02

## 1. Instalação
Certifique-se de estar na raiz do projeto `exercicio_02/`.

```bash
pip install -r requirements.txt
```

## 2. Treinamento (Obrigatório)
Diferente de scripts de exemplo comuns, esta API **não funciona** sem o modelo serializado. Execute o script de treinamento para gerar o artefato:

```bash
python train/train.py
```
*Este script baixará o dataset da UCI automaticamente via biblioteca `ucimlrepo`.*

## 3. Execução da API
Com o arquivo `model/modelo_energia.joblib` gerado, inicie a API:

```bash
uvicorn app.main:app --reload
```

## 4. Testando a API
Acesse a documentação interativa em: `http://127.0.0.1:8000/docs`

### Exemplo de Payload Válido:
```json
{
  "relative_compactness": 0.98,
  "surface_area_m2": 514.5,
  "wall_area_m2": 294.0,
  "roof_area_m2": 110.25,
  "overall_height_m": 7.0,
  "orientation": 2,
  "glazing_area_pct": 0.0,
  "glazing_area_distribution": 0
}
```

## 6. Docker (Apenas Ilustrativo)
O `Dockerfile` incluído neste repositório serve apenas para **demonstrar** como seria o empacotamento da aplicação. **Não utilize o Docker como forma primária de execução deste exercício**, pois o foco é o entendimento do fluxo local via `.venv`.
