import duckdb
from contextlib import contextmanager
import os
import re
# from ezorm import DATABASE
# Context Manager for DuckDB Connection
@contextmanager
def duck_connection(database:str):
    """A context manager to manage DuckDB connections."""
    # Establish the connection
    conn = duckdb.connect(database=database)
    try:
        yield conn  # Yield the connection for usage
    finally:
        conn.close()  # Ensure the connection is closed after use

def remove_escape_characters(text:str)->str:
    pattern = r"[;]"
    return re.sub(pattern, "", text)

def create_directory(db_path:str)->None:
    directory = os.path.dirname(db_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

# def execute(query:str, data:list=[], response=False):
#     with duck_connection(database=DATABASE) as con:
#         records = con.execute(query, data).df()
#     if response==True:
#         return records