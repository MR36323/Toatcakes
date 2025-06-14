import pandas as pd
from boto3 import client
from datetime import datetime


def reformat(
    table: pd.DataFrame, bucket_name: str, table_name: str, s3_client: client
) -> dict:
    """Places transformed data into proccess zone bucket.

    Args:
        table: A pandas dataframe containing transformed data.
        bucket_name: A string naming the target s3 bucket.
        table_name: A string naming the table.
        s3_client: A boto3 s3 client.

    Returns:
        Dictionary containing return info from boto3client put_object.
    """

    my_datetime = str(datetime.now()).replace(" ", "-")
    parquet_format = table.to_parquet(engine="fastparquet")

    return s3_client.put_object(
        Bucket=bucket_name,
        Key=f"{table_name}/data-{my_datetime}.snappy.parquet",
        Body=parquet_format,
    )
