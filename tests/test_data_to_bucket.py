from utils.data_to_bucket import data_to_bucket, DataIsNoneError
import pytest
from moto import mock_aws
import boto3
import os

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

{'test_table': [{'test_column': 'test_value'}]}

# @pytest.mark.skip()
def test_throws_error_if_data_is_none(s3_client_with_bucket):
    with pytest.raises(DataIsNoneError) as exc:
        response = data_to_bucket(None, 'test_bucket', s3_client_with_bucket)
    assert str(exc.value) == 'Data must not be None'

@pytest.mark.skip()
def test_throws_error_if_given_invalid_bucket_name():
    ...

@pytest.mark.skip()
def test_function_uploads_object_to_bucket():
    ...

@pytest.mark.skip()
def test_that_s3_data_is_immutable():
    ...

@pytest.mark.skip()
def test_naming_convention_of_bucket_objects():
    ...