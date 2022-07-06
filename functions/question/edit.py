import boto3
import json
import functions.common.auth as auth
import functions.common.error as error
from flask import Blueprint, request

cognito = boto3.client("cognito-idp")
db = boto3.client("dynamodb")
question_edit_file = Blueprint("question_edit_file", __name__)

@question_edit_file.route("/quizzes/<quiz_id>/questions/<question_id>", methods=["PUT"])
def lambda_handler(quiz_id, question_id):
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

    error_out = error.question_not_found(db, question_id)
    if error_out is not None:
        return error_out

    body = json.loads(request.data)
    choices = []
    for choice in body["choices"]:
        choices.append({ "S": choice })

    error_out = error.answer_not_valid(choices, body["answers"], body["is_multiple"])
    if error_out is not None:
        return error_out

    answers = list(map(str, body["answers"]))
    db.put_item(TableName="Question", Item={
        "question_id": { "S": question_id },
        "quiz_id": { "S": quiz_id },
        "text": { "S": body["text"] },
        "is_mutiple": { "BOOL": body["is_multiple"] },
        "choices": { "L": choices },
        "answers": { "NS": answers }
    })

    return { "question_id": question_id }, 200
