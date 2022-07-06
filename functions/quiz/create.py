import boto3
import datetime
import json
import uuid
import functions.common.auth as auth
import functions.common.error as error
from flask import Blueprint, request

cognito = boto3.client("cognito-idp")
db = boto3.client("dynamodb")
quiz_create_file = Blueprint("quiz_create_file", __name__)

@quiz_create_file.route("/quizzes", methods=["POST"])
def lambda_handler():
    user_id, error_out = auth.validate_user(request.headers.get("Authorization"))
    if error_out is not None:
        return error_out

    error_out = error.title_empty(request.data)
    if error_out is not None:
        return error_out

    dt_str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    body = json.loads(request.data)
    quiz_id = str(uuid.uuid4())
    db.put_item(TableName="Quiz", Item={
        "quiz_id": { "S": quiz_id },
        "user_id": { "S": user_id },
        "timestamp": { "S": dt_str },
        "title": { "S": body["title"] },
        "questions": { "L": [] },
        "is_published": { "BOOL": False },
        "is_disabled": { "BOOL" : False }
    })

    return { "quiz_id": quiz_id }, 200
