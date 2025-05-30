import sys
sys.path.append('/opt/python')

from utils.fetch_data import make_connection, close_connection, get_data
from utils.data_to_bucket import data_to_bucket
import boto3


def lambda_handler(event, context):
    conn = make_connection()
    tables = [
        "counterparty",
        "currency",
        "department",
        "design",
        "staff",
        "sales_order",
        "address",
        "payment",
        "purchase_order",
        "payment_type",
        "transaction",
    ]

    input_data = {table_name: get_data(conn, f"SELECT * FROM {table_name}", table_name)[table_name] for table_name in tables}

    s3_client = boto3.client('s3')

    data_to_bucket(input_data, "ingestion-zone-bucket-20250530145907229100000002", s3_client)


    # for table in tables:
    #     query = f"SELECT * FROM {table}"
    #     result = get_data(conn, query, table)
    close_connection(conn)
