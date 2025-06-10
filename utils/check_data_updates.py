from boto3 import client
import os
from dotenv import load_dotenv
import json
from decimal import Decimal
from typing import Any, Dict
from datetime import datetime


def normalise(obj):
    if isinstance(obj, dict):
        return {key: normalise(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [normalise(i) for i in obj]
    elif isinstance(obj, (datetime, Decimal)):
        return str(obj)
    else:
        return obj


def check_data_updates(new_data):
    load_dotenv()

    s3_client = client("s3")

    table_name = list(new_data.keys())[0]

    objects_response = s3_client.list_objects_v2(
        Bucket=os.environ.get("INGESTION_BUCKET"), Prefix=table_name
    )
    if objects_response["KeyCount"] == 0:
        return True

    times_list = [obj["LastModified"] for obj in objects_response["Contents"]]

    most_recent = max(times_list)
    most_recent_key = [
        obj["Key"]
        for obj in objects_response["Contents"]
        if obj["LastModified"] == most_recent
    ][0]

    current_data = (
        s3_client.get_object(Bucket=os.environ.get("INGESTION_BUCKET"), Key=most_recent_key)[
            "Body"
        ]
        .read()
        .decode("utf-8")
    )
    json_current = json.loads(current_data)
    print("s3", json_current)
    print("db", new_data)
    if normalise(json_current) == normalise(new_data):
        return False
    else:
        return True
