from utils.load_data_to_warehouse import make_connection, close_connection, get_secret, reformat_and_upload
import pytest
from moto import mock_aws
from unittest.mock import Mock, patch
import pandas as pd
import boto3
import os




@patch("utils.load_data_to_warehouse.get_secret")
@patch("utils.load_data_to_warehouse.Connection")
def test_returns_connection_object(mock_connection, mock_secret):
    mock_conn = Mock()
    mock_connection.return_value = mock_conn
    mock_secret.return_value = {
        "username": "test_username",
        "password": "123",
        "engine": "postgres",
        "host": "test_host.amazonaws.com",
        "port": 5432,
        "dbname": "test_DB",
    }
    conn = make_connection()
    assert conn is mock_conn
    close_connection(conn)

# @pytest.fixture(scope="function")
# def rds_client(aws_credentials):
#     pass

# @pytest.fixture(scope="function")
# def rds_client_with_data(rds_client):
#     # INVESTIGATE FUNCTIONALITY TO MOCK AN RDS WITH DATA IN IT
#     pass

@patch("utils.load_data_to_warehouse.get_secret")
@patch("utils.load_data_to_warehouse.Connection")
def test_function_uploads_table_data_to_warehouse(mock_connection, mock_secret):
    mock_conn = Mock()
    mock_connection.return_value = mock_conn
    mock_secret.return_value = {
        "username": "test_username",
        "password": "123",
        "engine": "postgres",
        "host": "test_host.amazonaws.com",
        "port": 5432,
        "dbname": "test_DB",
    }
    test_table_name = "staff"
    test_dataframe = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    parquet_data = test_dataframe.to_parquet()
    result = reformat_and_upload(mock_connection, test_table_name, parquet_data)
    close_connection(mock_connection)

    assert result == 3

def test_naming_convention_of_new_table_data_uploads():
    pass

def test_function_replaces_existing_data():
    pass

def test_table_is_in_raw_based_binary_format():
    pass

def test_exception_is_raised_if_data_not_uploaded():
    pass