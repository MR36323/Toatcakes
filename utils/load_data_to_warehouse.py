from pg8000.native import Connection
from pg8000.exceptions import InterfaceError, DatabaseError
from dotenv import load_dotenv
from boto3 import client, session
from botocore.exceptions import ClientError
import json

# Note that data types in some columns may have to be changed to conform to the warehouse data model.

def make_connection():
    # GET SECRET FOR RDS
    load_dotenv()
    pass

def close_connection():
    pass

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
  
    session = session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(f"ERROR :{e}")
        raise e

    secret = get_secret_value_response["SecretString"]
    return json.loads(secret)

def reformat_and_upload(parquet_table: str, rds_endpoint, rds_client: client):
    # Gets passed in a parquet table format.
    # Change parquet format to dataframe.
    # Uses pd.DataFrame.to_sql() to replace the table in the rds with the updated table.

    # conn.run("CREATE TABLE IF NOT EXISTS test (id INT, name TEXT);")
    # conn.run("INSERT INTO test (id, name) VALUES (%s, %s);", (1, 'Alice'))
    # conn.commit() ?
    pass

