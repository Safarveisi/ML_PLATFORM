import os
from fastapi import FastAPI, Response
from postgres_conn import PostgresHandler

app = FastAPI()

# Liveness/Readiness prob 
@app.get("/healthz")
async def health_check() -> Response:
    return Response(content="ok", status_code=200)

@app.get("/select-api")
async def postgres_write(api_name: str) -> None:
    postgres_handler = PostgresHandler()
    postgres_handler.insert_into_postgres_table(api_name=api_name) 
