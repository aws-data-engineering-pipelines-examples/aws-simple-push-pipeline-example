import json

import boto3


def lambda_handler(event, context):
    event_id = event.get("id")
    s3 = boto3.resource("s3")
    s3_obj = s3.Object("simple-push-pipeline-bucket", f"{event_id}.json")

    s3_obj.put(Body=(bytes(json.dumps(event).encode("UTF-8"))))
    return {
        "statusCode": 200,
        "event": event,
    }
