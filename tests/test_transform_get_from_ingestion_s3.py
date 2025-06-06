from utils.transform_get_from_ingestion_s3 import get_data
import pytest
import os
import boto3
import json
from moto import mock_aws
from datetime import datetime
from unittest.mock import patch
import time


@pytest.fixture(scope="function", autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def s3_client(aws_credentials):
    with mock_aws():
        yield boto3.client("s3")


@pytest.fixture(scope="function")
def s3_client_with_bucket(s3_client):
    s3_client.create_bucket(Bucket="test-bucket")
    yield s3_client

@pytest.fixture(scope='function')
def s3_client_with_bucket_with_objects(s3_client_with_bucket):
    s3_client_with_bucket.put_object(Bucket='test-bucket', Key=f'test_table1{datetime(2025, 1, 1)}', Body=json.dumps({'test_table1': [{'test_column1': 'test_value1'}]}))
    time.sleep(1)
    s3_client_with_bucket.put_object(Bucket='test-bucket', Key=f'test_table1{datetime(2025, 1, 2)}', Body=json.dumps({'test_table1': [{'test_column2': 'test_value2'}]}))
    yield s3_client_with_bucket

@patch('utils.transform_get_from_ingestion_s3.client')
def test_returns_latest_list_of_values(mock_client, s3_client_with_bucket_with_objects):
    mock_client.return_value = s3_client_with_bucket_with_objects
    assert get_data('test_table1', 'test-bucket') == [{"test_column2": "test_value2"}]
