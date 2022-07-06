import boto3
import functions.common.auth as auth
import functions.common.error as error
from flask import Blueprint, request

cognito = boto3.client("cognito-idp")
db = boto3.client("dynamodb")
quiz_publish_file = Blueprint("quiz_publish_file", __name__)

@quiz_publish_file.route("/quizzes/<quiz_id>/publish", methods=["POST"])
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

    if len(quiz["questions"]["L"]) < 1:
        return {
            "message": "The quiz cannot be published because there is no question"
        }, 422

    db.update_item(TableName="Quiz", Key={
        "quiz_id": { "S": quiz_id }
    }, AttributeUpdates={
        "is_published": { "Value": { "BOOL": True }}
    })

    return { "quiz_id": quiz_id }, 200
