import boto3
import json
import functions.common.auth as auth
import functions.common.error as error
from flask import Blueprint, request

cognito = boto3.client("cognito-idp")
db = boto3.client("dynamodb")
quiz_edit_file = Blueprint("quiz_edit_file", __name__)

@quiz_edit_file.route("/quizzes/<quiz_id>", methods=["PUT"])
def lambda_handler(quiz_id):
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

    error_out = error.quiz_not_editable(quiz)
    if error_out is not None:
        return error_out

    error_out = error.title_empty(request.data)
    if error_out is not None:
        return error_out

    body = json.loads(request.data)
    db.update_item(TableName="Quiz", Key={
        "quiz_id": { "S": quiz_id }
    }, AttributeUpdates={
        "title": { "Value": { "S": body["title"] }}
    })

    return { "quiz_id": quiz_id }, 200
