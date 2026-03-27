# Instruções de Execução — Exercício 04 (Testes Automatizados)

## 1. Setup
Navegue para a pasta `exercicio_04/` e instale as dependências:

```bash
pip install -r requirements.txt
```

## 2. Treinamento
O modelo precisa ser treinado para gerar o artefato que a API e os testes de integração utilizam:

```bash
python train/train.py
```

## 3. Executando os Testes (O Coração deste Exercício)
Para rodar toda a suíte de testes e verificar se as regras de validação estão funcionando:

```bash
pytest tests
```
*Você verá 11 testes passando, cobrindo casos de idade inválida, colesterol absurdo e integração de API.*

## 4. Subindo a API
Se quiser testar manualmente via Swagger:

```bash
uvicorn app.main:app --reload
```
Tente enviar um JSON com `age: 150` no `/predict` e observe o erro detalhado.

### Exemplo de Payload Válido:
```json
{
  "age": 54,
  "sex": 1,
  "cp": 1,
  "trestbps": 120,
  "chol": 240,
  "thalach": 150
}
```
