from utils.fetch_data import (
    make_connection,
    close_connection,
    get_data,
    zip_rows_and_columns,
    get_secret,
)
from pg8000.exceptions import InterfaceError, DatabaseError
from datetime import datetime
import pytest
from unittest.mock import Mock, patch
from moto import mock_aws
import boto3
import json
from botocore.exceptions import ClientError


class TestMakeConnection:
    @patch("utils.fetch_data.get_secret")
    @patch("utils.fetch_data.Connection")
    def test_returns_a_connection_object(self, mock_connection, mock_secret):
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

    @patch("utils.fetch_data.get_secret")
    @patch("utils.fetch_data.Connection")
    def test_raises_exception(self, mock_connection, mock_secret):
        mock_secret.return_value = {
            "username": "test_username",
            "password": "123",
            "engine": "postgres",
            "host": "test_host.amazonaws.com",
            "port": 5432,
            "dbname": "test_DB",
        }
        mock_connection.side_effect = InterfaceError("test error")
        with pytest.raises(InterfaceError):
            make_connection()


class TestCloseConnections:

    def test_close_connection_raises_exception(self):
        mock_conn = Mock()
        mock_conn.close.side_effect = Exception("test error")
        with pytest.raises(Exception):
            close_connection(mock_conn)

    def test_close_connection_raises_interface_error(self):
        mock_conn = Mock()
        mock_conn.close.side_effect = InterfaceError("test error")
        with pytest.raises(InterfaceError):
            close_connection(mock_conn)

    def test_close_connection_raises_attribute_error(self):
        with pytest.raises(AttributeError):
            close_connection(None)


class TestZipRowsAndColumns:

    def test_on_empty_table(self):
        rows = []
        columns = ["A", "B", "C"]
        assert zip_rows_and_columns(rows, columns) == []

    def test_on_non_empty_table(self):
        rows = [[1, 2, "test_name"]]
        columns = ["A", "B", "C"]
        assert zip_rows_and_columns(rows, columns) == [
            {"A": 1, "B": 2, "C": "test_name"}
        ]

    def test_on_multi_row_table(self):
        rows = [[1, 2, "test_name1"], [3, 4, "test_name2"]]
        columns = ["A", "B", "C"]
        assert zip_rows_and_columns(rows, columns) == [
            {"A": 1, "B": 2, "C": "test_name1"},
            {"A": 3, "B": 4, "C": "test_name2"},
        ]


class TestGetData:

    def test_returns_dict_with_key_of_queried_table_name(self):
        mock_conn = Mock()
        mock_conn.columns = [
            {"name": "staff_id"},
            {"name": "first_name"},
            {"name": "last_name"},
            {"name": "created_at"},
        ]
        mock_conn.run.return_value = [
            (1, "Jeremie", "Franey", datetime(2022, 11, 3, 14, 20, 51, 563000))
        ]
        query = "SELECT * FROM staff"
        result = get_data(mock_conn, query, "staff")
        assert isinstance(result, dict)
        assert "staff" in result

    def test_returns_dict_containing_list_of_correct_length(self):
        mock_conn = Mock()
        mock_conn.columns = [
            {"name": "staff_id"},
            {"name": "first_name"},
            {"name": "last_name"},
            {"name": "created_at"},
        ]
        mock_conn.run.return_value = [
            (1, "J", "F", datetime(2022, 11, 3, 14, 20, 51, 563000)),
            (2, "D", "B", datetime(2022, 11, 3, 14, 20, 51, 563000)),
        ]
        query = "SELECT * FROM staff"
        result = get_data(mock_conn, query, "staff")
        assert isinstance(result["staff"], list)
        assert len(result["staff"]) == 2

    def test_returns_dict_containing_list_of_appropriate_items(self):
        mock_conn = Mock()
        mock_conn.columns = [
            {"name": "staff_id"},
            {"name": "first_name"},
            {"name": "last_name"},
            {"name": "created_at"},
        ]
        mock_conn.run.return_value = [
            (1, "J", "F", datetime(2022, 11, 3, 14, 20, 51, 563000)),
            (2, "D", "B", datetime(2022, 11, 3, 14, 20, 51, 563000)),
        ]
        query = "SELECT * FROM staff"
        result = get_data(mock_conn, query, "staff")
        for row in result["staff"]:
            assert isinstance(row, dict)
            assert "staff_id" in row
            assert "first_name" in row
            assert "last_name" in row
            assert "created_at" in row
            assert isinstance(row["staff_id"], int)
            assert isinstance(row["first_name"], str)
            assert isinstance(row["last_name"], str)
            assert isinstance(row["created_at"], datetime)

    def test_handles_table_with_no_rows(self):
        mock_conn = Mock()
        mock_conn.columns = [
            {"name": "staff_id"},
            {"name": "first_name"},
            {"name": "last_name"},
            {"name": "created_at"},
        ]
        mock_conn.run.return_value = []
        query = "SELECT * FROM staff"
        result = get_data(mock_conn, query, "staff")
        assert result == {"staff": []}

    def test_raises_exception_when_table_does_not_exist(self):
        mock_conn = Mock()
        mock_conn.run.side_effect = DatabaseError("table does not exist")
        query = "SELECT * FROM non_existent_table"
        with pytest.raises(DatabaseError):
            get_data(mock_conn, query, "non_existent_table")


class TestGetSecret:

    @mock_aws
    def test_retrieves_secret_from_aws_secret_manager(self):
        info = {
            "username": "test_username",
            "password": "123",
            "engine": "postgres",
            "host": "test_host.amazonaws.com",
            "port": 5432,
            "dbname": "test_DB",
        }
        info_json = json.dumps(info)

        conn = boto3.client("secretsmanager", region_name="eu-west-2")
        conn.create_secret(Name="test_secret", SecretString=info_json)
        result = get_secret("test_secret", "eu-west-2")
        assert result == info

    @mock_aws
    def test_throws_an_a_client_error_when_something_goes_wrong(self):

        with pytest.raises(ClientError):
            get_secret("test_secret", "eu-west-2")
