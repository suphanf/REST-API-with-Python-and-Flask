import boto3
import json
import common.auth as auth

db = boto3.client("dynamodb")

def lambda_handler(event, context):
    results = db.query(TableName="Quiz",
        IndexName="user_id-index",
        KeyConditionExpression="user_id = :user_id",
        ExpressionAttributeValues={
            ":user_id": { "S": auth.get_user_id(event) }
        }
    )
    
    quizzes = []
    for result in results["Items"]:
        quizzes.append({
            "quiz_id": result["quiz_id"]["S"],
            "title": result["title"]["S"],
            "timestamp": result["timestamp"]["S"],
            "is_published": result["is_published"]["BOOL"]
        })

    return {
        "statusCode": 200,
        "body": json.dumps(quizzes)
    }