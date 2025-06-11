from botocore.exceptions import ClientError
from boto3 import client
import json
import os
from dotenv import load_dotenv


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
    for data_point in json_current[table_name]:
        for key in list(data_point.keys()):
            try:
                data_point[key] = data_point[key].replace("'", "''")
                # data_point[key] = f"'{data_point[key]}'"
            except AttributeError:
                pass

    return json_current[table_name]


if __name__ == "__main__":
    load_dotenv()
    get_data("address", os.environ.get("INGESTION_BUCKET"))
