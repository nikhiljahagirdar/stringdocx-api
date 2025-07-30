import asyncpg
import os
from dotenv import load_dotenv
import pathlib

load_dotenv()


async def get_database() -> asyncpg.Connection:
    load_dotenv()
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    database=os.getenv("POSTGRES_DB", "wizdocx"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=int(os.getenv("POSTGRES_PORT", 5432)),
    connection_string="postgresql://{user}:{password}@{host}:{port}/{database}?sslmode=require"
    conn = await asyncpg.connect(connection_string)
    return conn


async def execute_sql_from_file():
    """
    Reads a .sql file from the given local path and executes its contents.
    """
    conn = await asyncpg.connect(
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        database=os.getenv("POSTGRES_DB", "wizdocx"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", 5432)),
    )

    # Define the local file path for scripts.sql
    file_path = os.path.join(os.path.dirname(__file__), "scripts.sql")
    if not pathlib.Path(file_path).is_file():
        raise FileNotFoundError(f"SQL file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as sql_file:
        sql_text = sql_file.read()

    result = await conn.execute(sql_text)
    return result
