import pandas as pd
from boto3 import client


def reformat(table: pd.DataFrame, bucket_name: str, s3_client: client) -> None:
    """Places transformed data into proccess zone bucket.

    Args: 
        table: A pandas dataframe containing transformed data. 
        bucket_name: A string naming the target s3 bucket.
        s3_client: A boto3 s3 client. 

    Returns:
        None.
    """
    ...