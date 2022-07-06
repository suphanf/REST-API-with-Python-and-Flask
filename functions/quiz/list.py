import boto3
import json
import functions.common.auth as auth
from flask import Blueprint, request

cognito = boto3.client("cognito-idp")
db = boto3.client("dynamodb")
quiz_list_file = Blueprint("quiz_list_file", __name__)

@quiz_list_file.route("/quizzes", methods=["GET"])
def lambda_handler():
    user_id, error_out = auth.validate_user(request.headers.get("Authorization"))
    if error_out is not None:
        return error_out

    results = db.query(TableName="Quiz",
        IndexName="user_id-index",
        KeyConditionExpression="user_id = :user_id",
        ExpressionAttributeValues={
            ":user_id": { "S": user_id }
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

    return json.dumps(quizzes), 200
