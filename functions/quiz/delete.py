import boto3
import json
import common.error as error

db = boto3.client("dynamodb")

def lambda_handler(event, context):
    error_out = error.quiz_id_missing(event)
    if error_out is not None:
        return error_out

    quiz_id = event["pathParameters"]["id"]
    error_out = error.quiz_not_found(db, quiz_id)
    if error_out is not None:
        return error_out

    quiz = db.get_item(TableName="Quiz", Key={
        "quiz_id": { "S": quiz_id }
    }).get("Item")
    error_out = error.quiz_not_creator(event, quiz)
    if error_out is not None:
        return error_out

    if quiz["is_published"]["BOOL"]:
        db.update_item(TableName="Quiz", Key={
            "quiz_id": { "S": quiz_id }
        }, AttributeUpdates={
            "is_disabled": { "Value": { "BOOL": True }}
        })
    else:
        db.delete_item(TableName="Quiz", Key={
            "quiz_id": { "S": quiz_id }
        })

    return {
        "statusCode": 200,
        "body": json.dumps({
            "quiz_id": quiz_id
        })
    }
