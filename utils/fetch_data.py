from pg8000.native import Connection
from pg8000.exceptions import InterfaceError, DatabaseError
import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
import json

def make_connection() -> Connection:
    """Connects to the database.

    Args:
      None.

    Returns:
      Pg8000 connection object.

    Raises:
      InterfaceError: If credentials are incorrect.
    """

    load_dotenv()
    try:
        conn = Connection(
            user=os.getenv("PG_USER"), 
            password=os.getenv("PG_PASSWORD"),
            database=os.getenv("PG_DATABASE"),
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT")
        )
        return conn
    except (InterfaceError, Exception) as e:
        print(f'An error occured: {e}')
        raise e

def close_connection(conn: Connection):
    """Closes connection to database.

    Args:
      conn: Pg8000 connection object.

    Returns:
      None.

    Raises:
      InterfaceError: When connection has been closed.
      AtrributeError: Argument is not connection object.
    """

    try:
        conn.close()
    except (AttributeError, InterfaceError, Exception) as e:
        print(f'An error occured: {e}')
        raise e

def zip_rows_and_columns(rows: list, columns: dict) -> list[dict]:
    """Maps the data in rows and column names.

    Args:
      rows: All rows in table.
      columns: All column names in table.

    Returns:
      Dictionary with data from rows and columns are mapped.
    """
    return [dict(zip(columns, row)) for row in rows]

def get_data(conn: Connection, query: str, table_name: str) -> dict:
    """Gets rows and columns from table in database.

    Args:
      conn: Pg8000 connection object.
      query: Selects all queries.
      table_name: Tables name.

    Returns:
      Dictionary with table name as key and data as value.

    Raises:
      DatabaseError: Table does not exist.
    """
    try:
        rows = conn.run(query)
        columns = [row['name'] for row in conn.columns]
        data = zip_rows_and_columns(rows, columns)
        return {table_name: data}
    except (DatabaseError, Exception) as e:
        print(f'An error occured: {e}')
        raise e
    

def get_secret(secret_name, region_name):
    
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
  

    return json.loads(secret)
