import datetime
import json

import boto3

JAVA_SQL_TIMESTAMP_FMT = "%Y-%m-%d %H:%M:%S"


def calculate_temperature_group(temperature: float) -> str:
    if 10 <= temperature < 20:
        return "A"
    elif 20 <= temperature < 30:
        return "B"
    else:
        return "C"


def parse_measurement_time(epoch: int) -> str:
    return datetime.datetime.fromtimestamp(epoch).strftime(JAVA_SQL_TIMESTAMP_FMT)


def lambda_handler(event, context):
    event_id = event.get("id")
    s3 = boto3.resource("s3")
    s3_obj = s3.Object("simple-push-pipeline-bucket", f"{event_id}.json")

    event["temp_group"] = calculate_temperature_group(event.get("temperature"))
    event["event_dt"] = parse_measurement_time(event.get("epoch"))
    event["ingestion_source"] = "aws-api"

    # save transformed event to S3 (no partitioning)
    s3_obj.put(Body=(bytes(json.dumps(event).encode("UTF-8"))))

    return {
        "statusCode": 200,
    }
