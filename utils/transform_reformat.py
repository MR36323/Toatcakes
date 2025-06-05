import pandas as pd
from boto3 import client
from datetime import datetime



def reformat(table: pd.DataFrame, bucket_name: str, s3_client: client) -> None:
    """Places transformed data into proccess zone bucket.

    Args: 
        table: A pandas dataframe containing transformed data. 
        bucket_name: A string naming the target s3 bucket.
        s3_client: A boto3 s3 client. 

    Returns:
        None.
    """
        
    my_datetime = str(datetime.now()).replace(' ', '-')
    parquet_format = table.to_parquet()

    return s3_client.put_object(Bucket=bucket_name, Key=f'data-{my_datetime}.snappy.parquet', Body=str(parquet_format))
