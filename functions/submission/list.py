import boto3
import json
import functions.common.auth as auth
import functions.common.error as error
from flask import Blueprint, request

cognito = boto3.client("cognito-idp")
db = boto3.client("dynamodb")
submission_list_file = Blueprint("submission_list_file", __name__)

@submission_list_file.route("/quizzes/<quiz_id>/submissions", methods=["GET"])
def list_by_quiz_id(quiz_id):
    user_id, error_out = auth.validate_user(request.headers.get("Authorization"))
    if error_out is not None:
        return error_out

    error_out = error.quiz_not_found(db, quiz_id)
    if error_out is not None:
        return error_out

    quiz = db.get_item(TableName="Quiz", Key={
        "quiz_id": { "S": quiz_id }
    }).get("Item")
    error_out = error.quiz_not_creator(user_id, quiz)
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
            "quiz_title": result["quiz_title"]["S"],
            "user_id": result["user_id"]["S"],
            "timestamp": result["timestamp"]["S"],
            "total_score": result["total_score"]["N"]
        })
    return json.dumps(submissions), 200

@submission_list_file.route("/submissions", methods=["GET"])
def list_by_user_id():
    user_id, error_out = auth.validate_user(request.headers.get("Authorization"))
    if error_out is not None:
        return error_out

    results = db.query(TableName="Submission",
        IndexName="user_id-quiz_id-index",
        KeyConditionExpression="user_id = :user_id",
        ExpressionAttributeValues={
            ":user_id": { "S": user_id }
        }
    )

    submissions = []
    for result in results["Items"]:
        submissions.append({
            "submission_id": result["submission_id"]["S"],
            "quiz_title": result["quiz_title"]["S"],
            "user_id": result["user_id"]["S"],
            "timestamp": result["timestamp"]["S"],
            "total_score": result["total_score"]["N"]
        })

    return json.dumps(submissions), 200
