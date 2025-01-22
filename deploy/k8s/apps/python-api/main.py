import os
from fastapi import FastAPI, Response
from postgres_conn import PostgresHandler

app = FastAPI()
postgres_handler = PostgresHandler()

# Liveness/Readiness prob 
@app.get("/healthz")
async def health_check() -> Response:
    return Response(content="ok", status_code=200)

# API endpoint
@app.get("/select-api")
async def postgres_write(api_name: str) -> None:
    if api_name.lower() in ("go", "node"):
        postgres_handler.insert_into_postgres_table(api_name=api_name)
    else:
        print("Skip writing to the postgres table.") 
