from pg8000.native import Connection
from pg8000.exceptions import InterfaceError, DatabaseError
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

    secrets_info = get_secret("prod/totesys", "eu-west-2")

    try:
        conn = Connection(
            user=secrets_info["username"],
            password=secrets_info["password"],
            database=secrets_info["dbname"],
            host=secrets_info["host"],
            port=secrets_info["port"]
        )
        return conn
    except (InterfaceError, Exception) as e:
        print(f"An error occured: {e}")
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
        print(f"An error occured: {e}")
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
        columns = [row["name"] for row in conn.columns]
        data = zip_rows_and_columns(rows, columns)
        return {table_name: data}
    except (DatabaseError, Exception) as e:
        print(f"An error occured: {e}")
        raise e


def get_secret(secret_name: str, region_name: str) -> dict:
    """Retrieves secret from the AWS secrets manager.

    Args:
      secret_name: Name of secret identifier.
      region_name: Region name for secrets manager.

    Returns:
      Dictionary with all the secrets info.

    Raises:
      ClientError: If anything goes wrong.
    """
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(f"ERROR :{e}")
        raise e

    secret = get_secret_value_response["SecretString"]
    return json.loads(secret)
