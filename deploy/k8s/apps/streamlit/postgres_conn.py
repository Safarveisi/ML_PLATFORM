import os
import pandas as pd
from sqlalchemy import create_engine

class PostgresHandler:

    def __init__(self) -> None:
        self.engine = create_engine(os.environ["DATABASE_URL"])

    def fetch_data(self) -> pd.DataFrame:
        with self.engine.connect() as conn, conn.begin():
            # Read all rows in public.request
            data = pd.read_sql_query("select * from public.request", conn)
            return data             