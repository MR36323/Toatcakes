from pg8000.native import Connection
from pg8000.exceptions import InterfaceError
import boto3
from botocore.exceptions import ClientError
import json


def make_connection():
    """Connects to the database.

    Args:
      None.

    Returns:
      Pg8000 connection object.

    Raises:
      InterfaceError: If credentials are incorrect.
    """

    secrets_info = get_secret("prod/warehouse", "eu-west-2")
    try:
        conn = Connection(
            user=secrets_info["username"],
            password=secrets_info["password"],
            database=secrets_info["dbname"],
            host=secrets_info["host"],
            port=secrets_info["port"],
        )
        return conn
    except (InterfaceError, Exception) as e:
        print(f"An error occured: {e}")
        raise e


def close_connection(conn):
    """Closes connection to database.

    Args:
      conn: Pg8000 connection object.

    Returns:
      None.
    conn.close()
    """


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
    client = session.client(
        service_name="secretsmanager", region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(f"ERROR :{e}")
        raise e

    secret = get_secret_value_response["SecretString"]
    return json.loads(secret)


def reformat_and_upload(
    conn: object, table_name: str, parquet_table: str
) -> int:
    """Adds data in parquet file to a psql table.

    Args:
      conn: pg8000 connection object.
      table_name: Name of table in psql database table.
      parquet_table: Data from a parquet file, corresponding to database table

    Returns:
      Number of rows in psql table.
    """

    df = parquet_table
    column_list = tuple(df.columns)
    column_list_items = "("
    for col in column_list:
        column_list_items += f"{str(col)}, "
    final_str = column_list_items.rstrip(", ") + ")"
    for index, row in df.iterrows():
        values = []
        for column in column_list:
            try:
                values.append(int(row[column]))
            except ValueError:
                values.append(f"'{str(row[column])}'")
            except TypeError:
                values.append(f"'{str('Null Value')}'")
        value_list_items = "("
        for value in values:
            value_list_items += f"{str(value)}, "

        value_str = value_list_items.rstrip(", ") + ")"

        query = f"INSERT INTO {table_name} {final_str} VALUES {value_str}"
        response = conn.run(query)
    query = f"SELECT COUNT(*) FROM {table_name}"
    response = conn.run(query)
    return response[0][0]
