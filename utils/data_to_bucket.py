from boto3 import client
from datetime import datetime
from botocore.exceptions import ClientError
import json


class DataIsNoneError(Exception):
    pass


class InvalidBucketError(Exception):
    pass


def data_to_bucket(
    data: dict[str, list[dict]], bucket_name: str, s3_client: client
) -> None:
    """Places extracted data in specified s3 bucket.

    Args:
        data: A json-complient dictionary containing data extracted
            from relational db. The keys, of type str, name tables
            in the db. The values, of type lists of dicts, contain
            the data of the corresponding db.
        bucket_name: A string naming the target s3 bucket.
        s3_client: A boto3 s3 client.

    Returns:
        None.

    Raises:
        DataIsNoneError: No data provided.
        InvalidBucketError: No bucket of that name exists.
    """
    if data is None:
        raise DataIsNoneError("Data must not be None")

    table_name = list(data.keys())[0]

    my_datetime = str(datetime.now()).replace(" ", "-")
    try:
        return s3_client.put_object(
            Bucket=bucket_name,
            Key=f"{table_name}/{my_datetime}.json",
            Body=json.dumps(data, default=str).encode("utf-8"),
        )

    except ClientError as exc:
        error_message = exc.response["Error"]["Code"]
        if error_message == "NoSuchBucket":
            raise
