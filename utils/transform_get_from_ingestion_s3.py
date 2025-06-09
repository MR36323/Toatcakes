from botocore.exceptions import ClientError
from boto3 import client
import json


def get_data(table_name: str, bucket_name: str) -> list:
    """Fetches data of table from ingestion zone.

    Args:
      table_name: A string representing the table name.
      bucket_name: A string representing the bucket name.

    Returns:
      A json-complient string of data from table.

    Raises:
      botocore.exceptions.ClientError.
    """
    s3_client = client("s3")

    objects_response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=table_name)
    # if objects_response['Contents'] == []
    print(objects_response["Contents"])

    times_list = [obj["LastModified"] for obj in objects_response["Contents"]]

    most_recent = max(times_list)

    most_recent_key = [
        obj["Key"]
        for obj in objects_response["Contents"]
        if obj["LastModified"] == most_recent
    ][0]

    current_data = (
        s3_client.get_object(Bucket=bucket_name, Key=most_recent_key)["Body"]
        .read()
        .decode("utf-8")
    )

    json_current = json.loads(current_data)
    return json_current[table_name]
