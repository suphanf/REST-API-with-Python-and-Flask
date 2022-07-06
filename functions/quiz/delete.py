import boto3
import functions.common.auth as auth
import functions.common.error as error
from flask import Blueprint, request

cognito = boto3.client("cognito-idp")
db = boto3.client("dynamodb")
quiz_delete_file = Blueprint("quiz_delete_file", __name__)

@quiz_delete_file.route("/quizzes/<quiz_id>", methods=["DELETE"])
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
        for question_id in map(lambda x: x["S"], quiz["questions"]["L"]):
            db.delete_item(TableName="Question", Key={
                "question_id": { "S": question_id }
            })

    return { "quiz_id": quiz_id }, 200
