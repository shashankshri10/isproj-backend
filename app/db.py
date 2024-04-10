import os
import asyncpg
from dotenv import load_dotenv
load_dotenv()

DB_USER = os.getenv("DB_USER") 
DB_PASS = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_USER = "postgres" 
DB_PASS = "1609@r"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "prac_db"

# returns a cursor object "conn", to run queries values=conn.fetch(...)
async def connect_to_pg():
    try:
        # print(f"{DB_USER}")
        conn = await asyncpg.connect(user=DB_USER, password=DB_PASS, database=DB_NAME, host=DB_HOST)
        print("Database connected")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
async def close_pg_connection(conn):
    await conn.close()