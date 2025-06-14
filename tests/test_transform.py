from src.transform import lambda_handler
from moto import mock_aws
from unittest.mock import patch
import os
import pytest
import pandas as pd
import boto3


@pytest.fixture(scope="function", autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["INGESTION_BUCKET"] = "test-ingestion-bucket"
    os.environ["PROCESSED_BUCKET"] = "test-processed-bucket"


@pytest.fixture(scope="function")
def s3_client(aws_credentials):
    with mock_aws():
        yield boto3.client("s3")


@patch("src.transform.get_data")
@patch("src.transform.create_dim_staff")
@patch("src.transform.create_dim_counterparty")
@patch("src.transform.create_dim_currency")
@patch("src.transform.create_dim_design")
@patch("src.transform.create_dim_location")
@patch("src.transform.create_dim_date")
@patch("src.transform.get_latest_transformed_object_from_S3")
@patch("src.transform.create_fact_sales_order")
@patch("src.transform.reformat")
def test_inputs_to_df_funcs(
    mock_reformat,
    mock_fact_sales,
    mock_latest,
    mock_date,
    mock_loc,
    mock_design,
    mock_currency,
    mock_counterparty,
    mock_staff,
    mock_get_data,
):
    mock_get_data.side_effect = [
        [{f"id{i}": f"val{i}", f"col{i}": f"val{i}"}] for i in range(1, 8)
    ]
    lambda_handler({}, {})

    staff_args = mock_staff.call_args[0]
    assert staff_args[0] == [{"id5": "val5", "col5": "val5"}]
    assert staff_args[1] == [{"id3": "val3", "col3": "val3"}]

    counterparty_args = mock_counterparty.call_args[0]
    assert counterparty_args[0] == [{"id1": "val1", "col1": "val1"}]
    assert counterparty_args[1] == [{"id7": "val7", "col7": "val7"}]

    currency_args = mock_currency.call_args[0]
    assert currency_args[0] == [{"id2": "val2", "col2": "val2"}]

    design_args = mock_design.call_args[0]
    assert design_args[0] == [{"id4": "val4", "col4": "val4"}]

    location_args = mock_loc.call_args[0]
    assert location_args[0] == [{"id7": "val7", "col7": "val7"}]

    date_args = mock_date.call_args[0]
    assert date_args[0] == [{"id6": "val6", "col6": "val6"}]

    fact_sales_args = mock_fact_sales.call_args[0]
    assert fact_sales_args[0] == [{"id6": "val6", "col6": "val6"}]


@patch("src.transform.get_data")
@patch("src.transform.create_dim_staff")
@patch("src.transform.create_dim_counterparty")
@patch("src.transform.create_dim_currency")
@patch("src.transform.create_dim_design")
@patch("src.transform.create_dim_location")
@patch("src.transform.create_dim_date")
@patch("src.transform.get_latest_transformed_object_from_S3")
@patch("src.transform.create_fact_sales_order")
@patch("src.transform.reformat")
def test_funcs_called_required_amount(
    mock_reformat,
    mock_fact_sales,
    mock_latest,
    mock_date,
    mock_loc,
    mock_design,
    mock_currency,
    mock_counterparty,
    mock_staff,
    mock_get_data,
):
    mock_get_data.side_effect = [
        [{f"id{i}": f"val{i}", f"col{i}": f"val{i}"}] for i in range(1, 8)
    ]
    lambda_handler({}, {})
    funcs = [
        mock_counterparty,
        mock_currency,
        mock_date,
        mock_design,
        mock_fact_sales,
        mock_staff,
        mock_loc,
        mock_latest,
    ]
    assert all(item.call_count == 1 for item in funcs)
    assert mock_get_data.call_count == 7
    assert mock_reformat.call_count == 7


@patch("src.transform.client")
@patch("src.transform.get_data")
@patch("src.transform.create_dim_staff")
@patch("src.transform.create_dim_counterparty")
@patch("src.transform.create_dim_currency")
@patch("src.transform.create_dim_design")
@patch("src.transform.create_dim_location")
@patch("src.transform.create_dim_date")
@patch("src.transform.get_latest_transformed_object_from_S3")
@patch("src.transform.create_fact_sales_order")
@patch("src.transform.reformat")
def test_reformat_takes_correct_args(
    mock_reformat,
    mock_fact_sales,
    mock_latest,
    mock_date,
    mock_loc,
    mock_design,
    mock_currency,
    mock_counterparty,
    mock_staff,
    mock_get_data,
    mock_client,
    s3_client,
):
    mock_staff.return_value = pd.DataFrame([{"staff_id": ["val1", "val2"]}])
    mock_counterparty.return_value = pd.DataFrame(
        [{"cp_id": ["val1", "val2"]}]
    )
    mock_currency.return_value = pd.DataFrame([{"curr_id": ["val1", "val2"]}])
    mock_design.return_value = pd.DataFrame([{"des_id": ["val1", "val2"]}])
    mock_loc.return_value = pd.DataFrame([{"loc_id": ["val1", "val2"]}])
    mock_date.return_value = pd.DataFrame([{"date_id": ["val1", "val2"]}])
    mock_fact_sales.return_value = pd.DataFrame(
        [{"fact_id": ["val1", "val2"]}]
    )
    mock_client.return_value = s3_client
    lambda_handler({}, {})
    args = mock_reformat.call_args[0]
    assert args[0].equals(pd.DataFrame([{"fact_id": ["val1", "val2"]}]))
    assert args[1] == "test-processed-bucket"
    assert args[2] == "fact_sales_order"
    assert args[3] == s3_client
