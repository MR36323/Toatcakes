import sys
import os
from dotenv import load_dotenv
from boto3 import client
from botocore.exceptions import ClientError
from utils.transform_transform import (
    create_dim_staff,
    create_dim_counterparty,
    create_dim_currency,
    create_dim_design,
    create_dim_location,
    create_dim_date,
    create_fact_sales_order,
    get_latest_transformed_object_from_S3,
)
from utils.transform_reformat import reformat
from utils.transform_get_from_ingestion_s3 import get_data


sys.path.append("/opt/python")


def lambda_handler(event, context) -> list:
    """
    Lambda handler reformating data from ingestion zone bucket,
    and putting it into the processed zone bucket.

    Args:
      event: Dict containing the Lambda function event data.
      context: Lambda runtime context.

    Returns:
      List containing dictionary containing return info from
      boto3client put_object.

    Raises:
      botocore.exceptions.ClientError
    """

    load_dotenv()
    tables = [
        "counterparty",
        "currency",
        "department",
        "design",
        "staff",
        "sales_order",
        "address",
    ]
    input_data = {
        table_name: get_data(table_name, os.environ.get("INGESTION_BUCKET"))
        for table_name in tables
    }
    dim_staff_df = create_dim_staff(
        input_data["staff"], input_data["department"]
    )
    dim_counterparty_df = create_dim_counterparty(
        input_data["counterparty"], input_data["address"]
    )
    dim_currency_df = create_dim_currency(input_data["currency"])
    dim_design_df = create_dim_design(input_data["design"])
    dim_location_df = create_dim_location(input_data["address"])
    dim_date_df = create_dim_date(input_data["sales_order"])
    previous_fact_df = get_latest_transformed_object_from_S3()
    fact_sales_df = create_fact_sales_order(
        input_data["sales_order"], previous_fact_df
    )
    dataframes = {
        "dim_staff": dim_staff_df,
        "dim_counterparty": dim_counterparty_df,
        "dim_currency": dim_currency_df,
        "dim_design": dim_design_df,
        "dim_location": dim_location_df,
        "dim_date": dim_date_df,
        "fact_sales_order": fact_sales_df,
    }
    s3_client = client("s3")
    try:
        responses = [
            reformat(
                dataframes[key],
                os.environ.get("PROCESSED_BUCKET"),
                key,
                s3_client,
            )
            for key in list(dataframes.keys())
        ]
    except ClientError:
        raise ClientError
    return responses
