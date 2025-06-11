from pg8000.native import Connection
from pg8000.exceptions import InterfaceError, DatabaseError
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
import pandas as pd
from io import BytesIO
import json

# Note that data types in some columns may have to be
# changed to conform to the warehouse data model.

def make_connection():
    
    secrets_info = get_secret("prod/warehouse", "eu-west-2")
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
    

def close_connection(conn):
    conn.close()

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

# def reformat_and_upload(parquet_table: str, rds_endpoint, rds_client: client):
def reformat_and_upload(conn: object, table_name: str, parquet_table: str):

    # df = pd.read_parquet(BytesIO(parquet_table))
    df = parquet_table
    query = f"TRUNCATE {table_name};"
    conn.run(query)

    # INSERT INTO staff ("A", "B") VALUES (1, 1)
    column_list = tuple(df.columns)
    column_list_items = '('
    for col in column_list:
        column_list_items += f'{str(col)}, '
    final_str = column_list_items.rstrip(', ') + ')'
    for index, row in df.iterrows():
        values = []
        for column in column_list:
            values.append(int(row[column]))
        
        values = tuple(values)
        query = f"INSERT INTO {table_name} {final_str} VALUES {values}"
        response = conn.run(query)
    query = f"SELECT COUNT(*) FROM {table_name}"
    response = conn.run(query)
    return response[0][0]


    # Gets passed in a parquet table format.
    # Change parquet format to dataframe.
    # Uses pd.DataFrame.to_sql() to replace the table in the rds with the updated table.

    # conn.run("CREATE TABLE IF NOT EXISTS test (id INT, name TEXT);")
    # conn.run("INSERT INTO test (id, name) VALUES (%s, %s);", (1, 'Alice'))
    # conn.commit() ?

