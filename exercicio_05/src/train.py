from ucimlrepo import fetch_ucirepo
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder
import joblib
import os


def train_model():
    print("Baixando dataset Car Evaluation da UCI...")
    car_evaluation = fetch_ucirepo(id=19)

    X = car_evaluation.data.features
    y = car_evaluation.data.targets

    # Definindo a ordem das categorias para o OrdinalEncoder
    categories = [
        ['low', 'med', 'high', 'vhigh'],      # buying
        ['low', 'med', 'high', 'vhigh'],      # maint
        ['2', '3', '4', '5more'],             # doors
        ['2', '4', 'more'],                   # persons
        ['small', 'med', 'big'],              # lug_boot
        ['low', 'med', 'high']                # safety
    ]

    pipeline = Pipeline([
        ('encoder', OrdinalEncoder(categories=categories)),
        ('classifier', RandomForestClassifier(
            n_estimators=100,
            random_state=42
        ))
    ])

    print("Treinando o modelo...")
    pipeline.fit(X, y.values.ravel())

    # Criar diretório models se não existir
    os.makedirs('models', exist_ok=True)

    model_path = 'models/car_model.joblib'
    joblib.dump(pipeline, model_path)
    print(f"Modelo salvo com sucesso em: {model_path}")


if __name__ == "__main__":
    train_model()
