from pg8000.native import Connection
from pg8000.exceptions import InterfaceError
import os
from dotenv import load_dotenv

def make_connection():
    load_dotenv()
    try:
        conn = Connection(
            user=os.getenv("PG_USER"), 
            password=os.getenv("PG_PASSWORD"),
            database=os.getenv("PG_DATABASE"),
            host=os.getenv("PG_HOST"),
            port=int(os.getenv("PG_PORT"))
        )
        return conn
    except Exception as e:
        print(f'An error occured: {e}')
        return None

def close_connection(conn):
    try:
        conn.close()
    except (AttributeError, InterfaceError, Exception) as e:
        print(f'An error occured: {e}')
        raise e

def get_data(conn, query,table_name):
    result = {}
    try:
        rows = conn.run(query)
        columns = [row['name'] for row in conn.columns]
        data = [dict(zip(columns, row)) for row in rows]
        result[table_name] = data
        return result
    except Exception as e:
        print(f'An error occured: {e}')
        return {}   

