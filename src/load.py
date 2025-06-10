from utils.load_get_from_processed_s3 import get_data
from utils.load_data_to_warehouse import reformat_and_upload, make_connection, close_connection
import os
from dotenv import load_dotenv

def lambda_handler(event, context):
    # Use similar functionality to extract lambda handler.
    tables = [
        "dim_counterparty",
        "dim_currency",
        "dim_design",
        "dim_staff",
        "fact_sales",
        "dim_location",
        "dim_date"
    ]
    conn = make_connection()
    load_dotenv()
    for table in tables:
        data = get_data(table, os.environ.get('PROCESSED_BUCKET'))
        reformat_and_upload(conn, table, data)
    close_connection()