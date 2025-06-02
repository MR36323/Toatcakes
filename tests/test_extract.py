from src.extract import lambda_handler
from moto import mock_aws
from unittest.mock import patch, Mock

@patch("src.extract.close_connection")
@patch("src.extract.make_connection")
def test_make_and_close_connection_are_called_once(mock_make_connection, mock_close_connection):
    lambda_handler({}, {})
    assert mock_make_connection.call_count == 1
    assert mock_close_connection.call_count == 1

@patch("src.extract.get_data")
@patch("src.extract.make_connection")
def test_data_gets_called_once_per_table(mock_make_connection, mock_get_data):
    mock_conn = Mock()
    mock_make_connection.return_value = mock_conn
    lambda_handler({}, {})
    assert mock_get_data.call_count == 11

@patch("src.extract.data_to_bucket")
@patch("src.extract.boto3.client")
@patch("src.extract.get_data")
@patch("src.extract.make_connection")
def test_format_of_input_data_is_correct(mock_make_connection, mock_get_data, mock_s3_client, mock_data_to_bucket):
    mock_conn = Mock()
    mock_client = Mock()
    mock_make_connection.return_value = mock_conn
    mock_s3_client.return_value = mock_client
    
    def fake_get_data(conn, query, table_name):
        fake_data = {table_name: [{"staff_first_name": "matthew", "staff_last_name": "burns"}, {"staff_first_name": "beth", "staff_last_name": "suffield"}]}
        return fake_data
    
    mock_get_data.side_effect = fake_get_data
    lambda_handler({}, {})
    input_data_arg = mock_data_to_bucket.call_args[0][0]
    assert "counterparty" in input_data_arg
    assert input_data_arg["staff"][0]["staff_first_name"] == "matthew"

@patch("src.extract.data_to_bucket")
@patch("src.extract.boto3.client")
@patch("src.extract.get_data")
@patch("src.extract.make_connection")
def test_data_to_bucket_is_called_with_correct_arguments(mock_make_connection, mock_get_data, mock_s3_client, mock_data_to_bucket):
    mock_conn = Mock()
    mock_client = Mock()
    mock_make_connection.return_value = mock_conn
    mock_s3_client.return_value = mock_client
    
    def fake_get_data(conn, query, table_name):
        fake_data = {table_name: [{"staff_first_name": "matthew", "staff_last_name": "burns"}, {"staff_first_name": "beth", "staff_last_name": "suffield"}]}
        return fake_data
    
    mock_get_data.side_effect = fake_get_data
    lambda_handler({}, {})
    input_data_args = mock_data_to_bucket.call_args[0]
    assert isinstance(input_data_args[0], dict)
    assert input_data_args[1] == 'ingestion-zone-bucket-20250530145907229100000002'
    assert input_data_args[2] == mock_client

@patch("src.extract.boto3.client")
@patch("src.extract.get_data")
@patch("src.extract.make_connection")
def test_s3_client_is_created(mock_make_connection, mock_get_data, mock_s3_client):
    mock_conn = Mock()
    mock_make_connection.return_value = mock_conn

    def fake_get_data(conn, query, table_name):
        fake_data = {table_name: [{"staff_first_name": "matthew", "staff_last_name": "burns"}, {"staff_first_name": "beth", "staff_last_name": "suffield"}]}
        return fake_data
    
    mock_get_data.side_effect = fake_get_data

    lambda_handler({}, {})

    assert mock_s3_client.call_count == 1
