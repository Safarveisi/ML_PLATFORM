import os
import boto3
import tempfile
import argparse
from typing import Dict

from pydantic_settings import BaseSettings

import pandas as pd
import xgboost as xgb

from ray import serve
from kserve import Model, ModelServer, model_server
from kserve.ray import RayModel


class EnvSettings(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    s3_endpoint_url: str
    s3_bucket: str
    s3_region: str
    experiment_id: str
    run_id: str

    @property
    def model_key(self) -> str:
        return f"ml_platform/mlartifacts/{self.experiment_id}/{self.run_id}/artifacts/iris_xgb/model.json"

settings = EnvSettings()


@serve.deployment(name="custom-model", num_replicas=1)
class XGBoostModel(Model):
    def __init__(self, name):
        super().__init__(name)
        self.ready = False
        self.download_xgb_model()

    def download_xgb_model(self) -> None:
        s3 = boto3.client(
            service_name="s3",
            region_name=settings.s3_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            endpoint_url=settings.s3_endpoint_url,
        )
        self.model = xgb.XGBClassifier()
        with tempfile.NamedTemporaryFile("wb") as f:
            s3.download_fileobj(settings.s3_bucket, settings.model_key, f)
            f.seek(0)
            self.model.load_model(f.name)

        self.ready = True

    async def predict(self, payload: Dict, headers: Dict[str, str] = None) -> Dict:
        inputs = payload["instances"]
        df = pd.DataFrame(inputs)
        output = self.model.predict(df)
        return {"predictions": output.tolist()}


parser = argparse.ArgumentParser(parents=[model_server.parser])
args, _ = parser.parse_known_args()

if __name__ == "__main__":
    app = XGBoostModel.bind(name=args.model_name)
    handle = serve.run(app)
    model = RayModel(name=args.model_name, handle=handle)
    model.load()
    ModelServer().start([model])
