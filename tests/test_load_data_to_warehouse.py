from utils.load_data_to_warehouse import make_connection, close_connection, get_secret, reformat_and_upload
import pytest
from moto import mock_aws
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import boto3
import os
from dotenv import load_dotenv
from pg8000.native import Connection

# @pytest.fixture(scope="function", autouse=True)
# def aws_credentials():
#     """Mocked AWS Credentials for moto."""
#     os.environ["AWS_ACCESS_KEY_ID"] = "testing"
#     os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
#     os.environ["AWS_SECURITY_TOKEN"] = "testing"
#     os.environ["AWS_SESSION_TOKEN"] = "testing"
#     os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

# @pytest.fixture(scope="function")
# def rds_client(aws_credentials):
#     with mock_aws():
#         yield boto3.client("rds")

# @pytest.fixture(scope="function")
# def rds_client_with_instance(rds_client):
#     rds_client.create_db_instance(DBInstanceIdentifier = 'test_instance')
#     yield rds_client

# @pytest.fixture(scope="function")
# def rds_client_with_data(rds_client):

@pytest.fixture(scope='function',autouse=True)
def make_db():
    load_dotenv()
    conn = Connection(
        user=os.environ.get("PG_USER"),
        password=os.environ.get('PG_PASSWORD'),
        host=os.environ.get('PG_HOST'),
        port=os.environ.get('PG_PORT'),
        database='postgres'
    )
    drop_db = conn.run("""DROP DATABASE IF EXISTS test_database
              """)
    create_db = conn.run('CREATE DATABASE test_database')
    
    db_conn = Connection(
        user=os.environ.get("PG_USER"),
        password=os.environ.get('PG_PASSWORD'),
        host=os.environ.get('PG_HOST'),
        port=os.environ.get('PG_PORT'),
        database='test_database'
    )

    staff_table = db_conn.run("""
                           CREATE TABLE staff (
                           a VARCHAR, b VARCHAR)"""
                           )
    return db_conn






@patch("utils.load_data_to_warehouse.Connection")
@patch("utils.load_data_to_warehouse.get_secret")
def test_function_uploads_table_data_to_warehouse(mock_secret, mock_conn, make_db):
    # load_dotenv()
    # conn = Connection(
    #         user=os.environ.get('PG_USER'),
    #         password=os.environ.get('PG_PASSWORD'),
    #         host=os.environ.get('PG_HOST'),
    #         port=os.environ.get('PG_PORT')
    #     )
    # conn.run('DROP DATABASE IF EXISTS test_database;')
    # conn.run('CREATE DATABASE test_database')
    # close_connection(conn)
    load_dotenv()
    mock_secret.return_value = {
        "username": os.environ.get('PG_USER'),
        "password": os.environ.get('PG_PASSWORD'),
        "engine":  'postgres',
        "host":  os.environ.get('PG_HOST'),
        "port": os.environ.get('PG_PORT'),
        "dbname": os.environ.get('PG_DATABASE')
    }
    mock_conn.return_value = make_db
    conn = make_connection()
    test_table_name = "staff"
    test_dataframe = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    parquet_data = test_dataframe.to_parquet()
    result = reformat_and_upload(conn, test_table_name, parquet_data)
    close_connection(conn)

    assert result == 3

# def test_naming_convention_of_new_table_data_uploads():
#     pass

# def test_function_replaces_existing_data():
#     pass

# def test_table_is_in_raw_based_binary_format():
#     pass

# def test_exception_is_raised_if_data_not_uploaded():
#     pass


# @patch("utils.load_data_to_warehouse.get_secret")
# @patch("utils.load_data_to_warehouse.Connection")
# def test_returns_connection_object(mock_connection, mock_secret):
#     mock_conn = Mock()
#     mock_connection.return_value = mock_conn
#     mock_secret.return_value = {
#         "username": "test_user",
#         "password": "password",
#         "engine": "postgres",
#         "host": "test_host",
#         "port": 5432,
#         "dbname": "test_DB",
#     }
#     conn = make_connection()
#     assert conn is mock_conn
#     close_connection(conn)