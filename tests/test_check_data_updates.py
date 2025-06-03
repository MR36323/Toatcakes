from utils.check_data_updates import check_data_updates
import pytest
import os
from moto import mock_aws
import boto3
import datetime
from unittest.mock import patch
import json
import time

@pytest.fixture(scope='function',autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["BUCKET"] = "test-bucket"

@pytest.fixture(scope='function')
def s3_client(aws_credentials):
    with mock_aws():
        yield boto3.client('s3')

@pytest.fixture(scope='function')
def s3_client_with_bucket(s3_client):
    s3_client.create_bucket(Bucket='test-bucket')
    yield s3_client

@pytest.fixture(scope='function')
def s3_client_with_bucket_with_objects(s3_client_with_bucket):
    s3_client_with_bucket.put_object(Bucket='test-bucket', Key=f'test_table1{datetime.datetime(2025, 1, 1)}', Body=json.dumps({'test_table1': [{'test_column1': 'test_value1'}]}))
    time.sleep(1)
    s3_client_with_bucket.put_object(Bucket='test-bucket', Key=f'test_table1{datetime.datetime(2025, 1, 2)}', Body=json.dumps({'test_table1': [{'test_column2': 'test_value2'}]}))
    yield s3_client_with_bucket


@patch('utils.check_data_updates.client')
def test_returns_boolean(mock_client, s3_client_with_bucket_with_objects):
    mock_client.return_value = s3_client_with_bucket_with_objects
    test_data = {"test_table1": [{"test_column1": "test_value1"}]}
    assert isinstance(check_data_updates(test_data), bool)

@patch('utils.check_data_updates.client')
def test_returns_true_if_data_is_changed(mock_client, s3_client_with_bucket_with_objects):
    mock_client.return_value = s3_client_with_bucket_with_objects
    test_data = {'test_table1': [{'test_column1': 'test_value1'}]}
    assert check_data_updates(test_data) == True

@patch('utils.check_data_updates.client')
def test_returns_false_if_data_is_unchanged(mock_client, s3_client_with_bucket_with_objects):
    mock_client.return_value = s3_client_with_bucket_with_objects
    test_data = {'test_table1': [{'test_column2': 'test_value2'}]}
    assert check_data_updates(test_data) == False

@patch('utils.check_data_updates.client')
def test_returns_true_if_no_objects(mock_client, s3_client_with_bucket):
    mock_client.return_value = s3_client_with_bucket
    test_data = {'test_table1': [{'test_column2': 'test_value2'}]}
    assert check_data_updates(test_data) == True

#check if prefix is working by adding more test tables