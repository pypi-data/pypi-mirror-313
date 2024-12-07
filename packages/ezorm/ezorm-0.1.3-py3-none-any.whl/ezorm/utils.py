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

def data_mapping(engine='duck'):
    if engine=='duck':
        return {
            str: "TEXT",    # or "TEXT" for unlimited length
            int: "INTEGER",
            float: "FLOAT",    # or "REAL" depending on the database
            bool: "BOOLEAN",
            # "datetime": "DATETIME"  # Use "TIMESTAMP" for PostgreSQL
        }
    elif engine=='prompt':
        return {
            str: "STRING",
            int: "INTEGER",
            float: "FLOAT",
            bool: "BOOLEAN"
        }
    else:
        raise ValueError(f"data_mapping only supports [duckdb, prompt], found '{engine}' instead")
    
def print_table(table:str, description:str, headers:list, rows:list)->list:
    str_table = []
    # Calculate column widths by finding the max length of each row in each column
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(headers, *rows)]

    # Create a format string for the table
    row_format = "| " + " | ".join(f"{{:<{width}}}" for width in col_widths) + " |"

    line = "-" * (sum(col_widths) + 3 * len(col_widths) + 1)
    str_table.append(line)
    str_table.append(f"Table: {table}")
    str_table.append(f"Description: {description}")
    str_table.append(line)
    str_table.append(row_format.format(*headers))
    str_table.append(line)
    for row in rows:
        str_table.append(row_format.format(*row))
    str_table.append(line)
    print("\n".join(str_table))
    return str_table