from utils.load_data_to_warehouse import (
    make_connection,
    close_connection,
    reformat_and_upload,
)
import pytest
from unittest.mock import patch, Mock
import pandas as pd
import os
from dotenv import load_dotenv
from pg8000.native import Connection


@pytest.fixture(scope="function", autouse=True)
def make_db():
    load_dotenv()
    conn = Connection(
        user=os.environ.get("PG_USER"),
        password=os.environ.get("PG_PASSWORD"),
        host=os.environ.get("PG_HOST"),
        port=os.environ.get("PG_PORT"),
        database="postgres",
    )
    conn.run(
        """DROP DATABASE IF EXISTS test_database
              """
    )
    conn.run("CREATE DATABASE test_database")

    db_conn = Connection(
        user=os.environ.get("PG_USER"),
        password=os.environ.get("PG_PASSWORD"),
        host=os.environ.get("PG_HOST"),
        port=os.environ.get("PG_PORT"),
        database="test_database",
    )

    db_conn.run(
        """
                           CREATE TABLE staff (
                           a VARCHAR, b VARCHAR)"""
    )
    return db_conn


@patch("utils.load_data_to_warehouse.Connection")
@patch("utils.load_data_to_warehouse.get_secret")
def test_function_uploads_table_data_to_warehouse(
    mock_secret, mock_conn, make_db
):
    load_dotenv()
    mock_secret.return_value = {
        "username": os.environ.get("PG_USER"),
        "password": os.environ.get("PG_PASSWORD"),
        "engine": "postgres",
        "host": os.environ.get("PG_HOST"),
        "port": os.environ.get("PG_PORT"),
        "dbname": os.environ.get("PG_DATABASE"),
    }
    mock_conn.return_value = make_db
    conn = make_connection()
    test_table_name = "staff"
    test_dataframe = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    parquet_data = test_dataframe.to_parquet()
    result = reformat_and_upload(conn, test_table_name, parquet_data)
    close_connection(conn)
    assert result == 3


@patch("utils.load_data_to_warehouse.get_secret")
@patch("utils.load_data_to_warehouse.Connection")
def test_returns_connection_object(mock_connection, mock_secret):
    mock_conn = Mock()
    mock_connection.return_value = mock_conn
    mock_secret.return_value = {
        "username": "test_user",
        "password": "password",
        "engine": "postgres",
        "host": "test_host",
        "port": 5432,
        "dbname": "test_DB",
    }
    conn = make_connection()
    assert conn is mock_conn
    close_connection(conn)
