from boto3 import client
import pandas as pd
from io import BytesIO


def get_data(table_name: str, bucket_name: str) -> pd.DataFrame:
    """Turns s3 bucket object into a Pandas Dataframe.

    Args:
      table_name: Name of table.
      bucket_name: Name of bucket containing table.

    Returns:
      Pandas DataFrame containing table contents.

    """

    try:
        s3_client = client("s3")
        objects_response = s3_client.list_objects_v2(
            Bucket=bucket_name, Prefix=table_name
        )

        times_list = [
            obj["LastModified"] for obj in objects_response["Contents"]
        ]
        most_recent = max(times_list)
        most_recent_key = [
            obj["Key"]
            for obj in objects_response["Contents"]
            if obj["LastModified"] == most_recent
        ][0]

        current_data = s3_client.get_object(
            Bucket=bucket_name, Key=most_recent_key
        )["Body"].read()
        parquet_data = pd.read_parquet(BytesIO(current_data))
        return parquet_data
    except Exception as e:
        print(f"An error occured: {e}")
        raise e
