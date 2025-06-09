from utils.load_data_to_warehouse import make_connection, close_connection, get_secret, reformat_and_upload
import pytest
from moto import mock_aws
import boto3
import os

@pytest.fixture(scope="function", autouse=True)
def aws_credentials():
    pass

@pytest.fixture(scope="function")
def rds_client(aws_credentials):
    pass

@pytest.fixture(scope="function")
def rds_client_with_data(rds_client):
    # INVESTIGATE FUNCTIONALITY TO MOCK AN RDS WITH DATA IN IT
    pass

def test_function_uploads_table_data_to_warehouse(rds_client_with_data):
    pass

def test_naming_convention_of_new_table_data_uploads(rds_client_with_data):
    pass

def test_function_replaces_existing_data(rds_client_with_data):
    pass

def test_table_is_in_raw_based_binary_format(rds_client_with_data):
    pass

def test_exception_is_raised_if_data_not_uploaded():
    pass