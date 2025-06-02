from src.extract import lambda_handler
import pytest
import os
from moto import mock_aws
import boto3


@pytest.fixture(scope='function',autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture(scope='function')
def s3_client(aws_credentials):
    with mock_aws():
        yield boto3.client('s3')

@pytest.fixture(scope='function')
def s3_client_with_bucket(s3_client):
    s3_client.create_bucket(Bucket='test_bucket')
    yield s3_client

def test_input_data_correct_format():
    pass

