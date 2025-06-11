from utils.load_get_from_processed_s3 import get_data
from utils.load_data_to_warehouse import (
    reformat_and_upload,
    make_connection,
    close_connection,
)
import os
from dotenv import load_dotenv


def lambda_handler(event, context):
    # Use similar functionality to extract lambda handler.
    deletion_tables = [
        "fact_sales_order",
        "dim_counterparty",
        "dim_currency",
        "dim_design",
        "dim_staff",
        "dim_location",
        "dim_date",
    ]

    tables = [
        "dim_counterparty",
        "dim_currency",
        "dim_design",
        "dim_staff",
        "dim_location",
        "dim_date",
        "fact_sales_order",
    ]
    conn = make_connection()
    load_dotenv()
    for table in deletion_tables:
        query = f"DELETE FROM {table};"
        conn.run(query)

    for table in tables:
        data = get_data(table, os.environ.get("PROCESSED_BUCKET"))
        reformat_and_upload(conn, table, data)
    close_connection(conn)


lambda_handler([], [])
