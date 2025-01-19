import os
import psycopg


class PostgresHandler:

    def __init__(self) -> None:
        self.db_url = os.environ["DATABASE_URL"]

    def insert_into_postgres_table(self, api_name: str) -> None:
        with psycopg.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                query = f"""INSERT INTO public.request (api_name)
                            VALUES (%s)"""
                cur.execute(query, (api_name,))
                conn.commit()
