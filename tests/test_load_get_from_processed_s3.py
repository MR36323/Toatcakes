from utils.load_get_from_processed_s3 import get_data
import pytest
import os
import boto3
from moto import mock_aws
from unittest.mock import Mock, patch
from botocore.exceptions import ClientError
from datetime import datetime
import pandas as pd
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
    

@pytest.fixture(scope="function")
def s3_client_with_bucket_with_objects(s3_client_with_bucket):
    test_dataframe = pd.DataFrame({"A": [1, 2, 3], "B": [1, 2, 3]})
    parquet_data = test_dataframe.to_parquet()
    s3_client_with_bucket.put_object(
        Bucket="test-bucket",
        Key=f"test_table1{datetime(2025, 1, 1)}",
        Body=parquet_data
    )
    time.sleep(1)
    test_dataframe2 = pd.DataFrame({"C": [1, 2, 3], "D": [1, 2, 3]})
    parquet_data2 = test_dataframe2.to_parquet()
    s3_client_with_bucket.put_object(
        Bucket="test-bucket",
        Key=f"test_table1{datetime(2025, 1, 1)}",
        Body=parquet_data2
    )
    yield s3_client_with_bucket

@patch("utils.load_get_from_processed_s3.client")
def test_returns_latest_table_objects(mock_client, s3_client_with_bucket_with_objects):
    mock_client.return_value = s3_client_with_bucket_with_objects
    result = get_data("test_table1", "test-bucket") 

    pd.testing.assert_frame_equal(result, pd.DataFrame({"C": [1, 2, 3], "D": [1, 2, 3]}))

@patch("utils.load_get_from_processed_s3.client")
def test_exception_is_raised_if_table_does_not_exist(mock_client, s3_client_with_bucket_with_objects):
    mock_client.return_value = s3_client_with_bucket_with_objects
    mock_client.side_effect = Exception("Simulated S3 client failure")
    with pytest.raises(Exception, match="Simulated S3 client failure"):
        get_data("test_table1", "test-bucket")
