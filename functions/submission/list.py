import boto3
import json
import common.auth as auth
import common.error as error

db = boto3.client("dynamodb")

def lambda_handler(event, context):
    if event["pathParameters"] is not None and "id" in event["pathParameters"]:
        return list_by_quiz_id(event, context)
    else:
        return list_by_user_id(event, context)

def list_by_quiz_id(event, context):
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

    results = db.query(TableName="Submission",
        IndexName="quiz_id-index",
        KeyConditionExpression="quiz_id = :quiz_id",
        ExpressionAttributeValues={
            ":quiz_id": { "S": quiz_id }
        }
    )

    submissions = []
    for result in results["Items"]:
        submissions.append({
            "submission_id": result["submission_id"]["S"],
            "timestamp": result["timestamp"]["S"],
            "total_score": result["total_score"]["N"]
        })
    return {
        "statusCode": 200,
        "body": json.dumps(submissions)
    }

def list_by_user_id(event, context):
    results = db.query(TableName="Submission",
        IndexName="user_id-quiz_id-index",
        KeyConditionExpression="user_id = :user_id",
        ExpressionAttributeValues={
            ":user_id": { "S": auth.get_user_id(event) }
        }
    )

    submissions = []
    for result in results["Items"]:
        submissions.append({
            "submission_id": result["submission_id"]["S"],
            "timestamp": result["timestamp"]["S"],
            "total_score": result["total_score"]["N"]
        })

    return {
        "statusCode": 200,
        "body": json.dumps(submissions)
    }
