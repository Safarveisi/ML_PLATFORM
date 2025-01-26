import requests
from starlette.requests import Request
from typing import Dict

from ray import serve

@serve.deployment(num_replicas=2)
class MyModelDeployment:
    def __init__(self, msg: str):
        # Initialize model state: could be very large neural net weights.
        self._msg = msg

    async def __call__(self, request: Request) -> Dict:
        return {"result": self._msg}

# 2: Deploy the application locally.
serve.run(MyModelDeployment.bind(msg="Hello world!"), route_prefix="/")

# 3: Query the application and print the result.
print(requests.get("http://localhost:8000/").json())