import os
from fastapi import FastAPI
from postgres_conn import PostgresHandler

app = FastAPI()

@app.get("/select-api")
async def postgres_write(api_name: str) -> None:
    postgres_handler = PostgresHandler()
    postgres_handler.insert_into_postgres_table(
        api_name=api_name
    )
