from boto3 import client
import os
from dotenv import load_dotenv
import json



def check_data_updates(new_data):
    load_dotenv()
    s3_client = client('s3')
    table_name = list(new_data.keys())[0]
    objects_response = s3_client.list_objects_v2(Bucket=os.environ.get('BUCKET'), Prefix=table_name)
    print(objects_response)
    times_list = [obj['LastModified'] for obj in objects_response['Contents']]
    most_recent = max(times_list)
    most_recent_key = [obj['Key'] for obj in objects_response['Contents'] if obj['LastModified'] == most_recent][0]
    current_data = s3_client.get_object(Bucket=os.environ.get('BUCKET'), Key=most_recent_key)['Body'].read().decode('utf-8')
    json_current = json.loads(current_data)
    if json_current == new_data:
        return False
    else:
        return True
