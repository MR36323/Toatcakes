from utils.load_get_from_processed_s3 import get_data
import pytest
import os
import boto3
from moto import mock_aws
from unittest.mock import patch

@pytest.fixture(scope="function", autouse=True)
def aws_credentials():
    pass

@pytest.fixture(scope="function")
def s3_client(aws_credentials):
    pass

@pytest.fixture(scope="function")
def s3_client_with_bucket(s3_client):
    pass

@pytest.fixture(scope="function")
def s3_client_with_bucket_with_objects(s3_client_with_bucket):
    pass

def test_returns_latest_table_objects(mock_client, s3_client_with_bucket_with_objects):
    pass

def test_returns_data_from_every_dim_and_fact_table():
    pass

# def test_returns_data_in_correct_format(): ????
#     pass

def test_exception_is_raised_correctly():
    pass