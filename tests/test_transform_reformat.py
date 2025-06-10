from utils.transform_reformat import reformat
import pytest
from moto import mock_aws
import boto3
import os
from unittest.mock import patch
from datetime import datetime
import pandas as pd
from io import BytesIO


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


# @pytest.mark.skip()
def test_function_uploads_object_to_bucket(s3_client_with_bucket):
    reformat(pd.DataFrame(), "test-bucket", 'test_table', s3_client_with_bucket)
    response = s3_client_with_bucket.list_objects_v2(Bucket="test-bucket")
    assert "data" in response["Contents"][0]["Key"]
    assert int(response["KeyCount"]) >= 1


def test_that_s3_data_is_immutable(s3_client_with_bucket):
    reformat(pd.DataFrame({"A": [1]}), "test-bucket", 'test_table', s3_client_with_bucket)
    reformat(pd.DataFrame({"B": [2]}), "test-bucket", 'test_table', s3_client_with_bucket)
    response = s3_client_with_bucket.list_objects_v2(Bucket="test-bucket")
    assert int(response["KeyCount"]) >= 2


# @pytest.mark.skip()
def test_naming_convention_of_bucket_objects(s3_client_with_bucket):  # =
    with patch("utils.transform_reformat.datetime") as dt:
        dt.now.return_value = datetime(2025, 5, 30)
        reformat(pd.DataFrame(), "test-bucket", 'test_table', s3_client_with_bucket)
    key = s3_client_with_bucket.list_objects_v2(Bucket="test-bucket")["Contents"][0][
        "Key"
    ]
    assert key == "test_table/data-2025-05-30-00:00:00.snappy.parquet"


def test_table_is_in_parquet_format(s3_client_with_bucket):
    test_dataframe = pd.DataFrame({"A": [1, 2, 3], "B": [1, 2, 3]})
    with patch("utils.transform_reformat.datetime") as dt:
        dt.now.return_value = datetime(2025, 5, 30)
        reformat(test_dataframe, "test-bucket", 'test_table', s3_client_with_bucket)

    key = s3_client_with_bucket.list_objects_v2(Bucket="test-bucket")["Contents"][0][
        "Key"
    ]
    bucket_object = s3_client_with_bucket.get_object(Bucket="test-bucket", Key=key)
    bucket_object = bucket_object["Body"].read()
    output = pd.read_parquet(BytesIO(bucket_object))
    pd.testing.assert_frame_equal(output, test_dataframe)
