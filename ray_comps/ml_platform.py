import mlflow
from mlflow.models import infer_signature

import sklearn.datasets
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import xgboost as xgb

import ray
from ray import train, tune
from ray.air.integrations.mlflow import setup_mlflow


def train_breast_cancer(config: dict) -> None:
    tracking_uri = config.pop("tracking_uri", None)
    experiment_name = config.pop("experiment_name", None)
    setup_mlflow(
        config,
        experiment_name=experiment_name,
        tracking_uri=tracking_uri,
    )
    # Load dataset
    data, labels = sklearn.datasets.load_breast_cancer(return_X_y=True)
    train_x, test_x, train_y, test_y = train_test_split(data, labels, test_size=0.2)

    model = xgb.XGBClassifier(**config)
    model.fit(train_x, train_y)

    predictions = model.predict(test_x)
    accuracy = accuracy_score(test_y, predictions)
    mlflow.log_metric("accuracy", accuracy)
    signature = infer_signature(train_x, model.predict(train_x))

    mlflow.xgboost.log_model(
        model,
        "xgb_models",
        conda_env=mlflow.xgboost.get_default_conda_env(),
        signature=signature,
        model_format="json",
    )

    train.report({"accuracy": accuracy, "done": True})


def tune_with_setup(mlflow_tracking_uri: str, experiment_name: str) -> None:

    mlflow.set_tracking_uri(mlflow_tracking_uri)
    mlflow.set_experiment(experiment_name=experiment_name)

    ray.init(num_cpus=6)
    trainable_with_resources = tune.with_resources(train_breast_cancer, {"cpu": 2})

    tuner = tune.Tuner(
        trainable_with_resources,
        tune_config=tune.TuneConfig(
            num_samples=10, 
        ),
        run_config=train.RunConfig(
            name="mlflow",
        ),
        param_space={
            "objective": "binary:logistic",
            "eval_metric": ["logloss", "error"],
            "max_depth": tune.randint(1, 9),
            "min_child_weight": tune.choice([1, 2, 3]),
            "subsample": tune.uniform(0.5, 1.0),
            "eta": tune.loguniform(1e-4, 1e-1),
            "tracking_uri": mlflow_tracking_uri,
            "experiment_name": experiment_name,
        },
    )

    tuner.fit()


tune_with_setup(
    mlflow_tracking_uri="http://0.0.0.0:5000", experiment_name="ml-platform"
)
