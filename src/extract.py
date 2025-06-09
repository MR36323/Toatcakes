import sys
from utils.fetch_data import make_connection, close_connection, get_data
from utils.data_to_bucket import data_to_bucket
from utils.check_data_updates import check_data_updates
import boto3
import os
from dotenv import load_dotenv

sys.path.append("/opt/python")


def lambda_handler(event, context):
    load_dotenv()
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

    # tables = conn.run("""SELECT * FROM information_schema.tables
    #                  WHERE table_schema = 'public'
    #                   AND table_name != '_prisma_migrations'""")
    # extra line

    s3_client = boto3.client("s3")
    for table in tables:
        new_data = get_data(conn, f"SELECT * FROM {table}", table)
        if check_data_updates(new_data):
            data_to_bucket(new_data, os.environ.get("BUCKET"), s3_client)
            data_to_bucket(new_data, os.environ.get("BUCKET"), s3_client)

    close_connection(conn)
