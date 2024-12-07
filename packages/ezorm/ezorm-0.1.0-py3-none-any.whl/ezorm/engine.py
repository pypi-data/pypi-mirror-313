import duckdb
from typing import Any
import pandas as pd
from ezorm.configuration import settings

def duck_engine(query:str, data:list=None, database:str=None)->pd.DataFrame:
    if database is None:
        database = settings.database
    with duckdb.connect(database) as con:
        return con.execute(query, data).df()