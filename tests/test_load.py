from src.load import lambda_handler
from unittest.mock import patch, Mock
import os
import pytest

@pytest.fixture(scope="function", autouse=True)
def aws_credentials():
    pass

@pytest.fixture(scope="function")
def s3_client(aws_credentials):
    pass

def test_s3_client_is_created():
    pass

def test_make_and_close_connection_to_warehouse_called_once():
    pass

def test_data_gets_called_once_per_dim_and_fact_table():
    pass

def test_format_of_input_data_to_warehouse_is_correct():
    pass

def test_data_to_warehouse_is_called_with_correct_arguments():
    pass