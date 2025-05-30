from utils.data_to_bucket import data_to_bucket, DataIsNoneError, InvalidBucketError
import pytest
from moto import mock_aws
import boto3
import os
from botocore.exceptions import ClientError

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

# @pytest.mark.skip()
def test_throws_error_if_data_is_none(s3_client_with_bucket):
    with pytest.raises(DataIsNoneError) as exc:
        data_to_bucket(None, 'test_bucket', s3_client_with_bucket)
    assert str(exc.value) == 'Data must not be None'

# @pytest.mark.skip()
def test_throws_error_if_given_invalid_bucket_name(s3_client_with_bucket):
    with pytest.raises(ClientError) as exc:
        data_to_bucket({'test_table': [{'test_column': 'test_value'}]}, 'random-bucket', s3_client_with_bucket)
    assert exc.value.response['Error']['Code'] == 'NoSuchBucket'

# @pytest.mark.skip()
def test_function_uploads_object_to_bucket(s3_client_with_bucket):
    data_to_bucket({'test_table': [{'test_column': 'test_value'}]}, 'test_bucket', s3_client_with_bucket)
    response = s3_client_with_bucket.list_objects_v2(Bucket='test_bucket')
    assert 'data' in response['Contents'][0]['Key']
    assert int(response['KeyCount']) >= 1

# @pytest.mark.skip()
def test_that_s3_data_is_immutable(s3_client_with_bucket):
    data_to_bucket({'test_table': [{'test_column': 'test_value'}]}, 'test_bucket', s3_client_with_bucket)
    data_to_bucket({'second_test_table': [{'second_test_column': 'second_test_value'}]}, 'test_bucket', s3_client_with_bucket)
    response = s3_client_with_bucket.list_objects_v2(Bucket='test_bucket')
    assert int(response['KeyCount']) >=2

@pytest.mark.skip()
def test_naming_convention_of_bucket_objects():
    ...

@pytest.mark.skip()
def test_format_of_data_is_correct():
    ...