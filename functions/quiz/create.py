import boto3
import datetime
import json
import uuid
import common.auth as auth
import common.error as error

db = boto3.client("dynamodb")

def lambda_handler(event, context):
    error_out = error.quiz_title_empty(event)
    if error_out is not None:
        return error_out

    dt_str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    body = json.loads(event["body"])
    quiz_id = str(uuid.uuid4())
    db.put_item(TableName="Quiz", Item={
        "quiz_id": { "S": quiz_id },
        "user_id": { "S": auth.get_user_id(event) },
        "timestamp": { "S": dt_str },
        "title": { "S": body["title"] },
        "questions": { "L": [] },
        "is_published": { "BOOL": False },
        "is_disabled": { "BOOL" : False }
    })

    return {
        "statusCode": 200,
        "body": json.dumps({
            "quiz_id": quiz_id
        })
    }
