import boto3
import json
import common.error as error

db = boto3.client("dynamodb")

def lambda_handler(event, context):
    quiz_id = event["pathParameters"]["id"]
    error_out = error.quiz_not_found(db, quiz_id)
    if error_out is not None:
        return error_out

    quiz = db.get_item(TableName="Quiz", Key={
        "quiz_id": { "S": quiz_id }
    }).get("Item")

    return {
      "statusCode": 200,
      "body": json.dumps({
          "title": quiz["title"],
          "timestamp": quiz["timestamp"],
          "questions": [],
          "is_published": quiz["is_published"]
      })
    }