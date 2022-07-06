import boto3
import json
import os
import uuid
import functions.common.auth as auth
import functions.common.error as error
from flask import Blueprint, request

cognito = boto3.client("cognito-idp")
db = boto3.client("dynamodb")
question_create_file = Blueprint("question_create_file", __name__)

@question_create_file.route("/quizzes/<quiz_id>/questions", methods=["POST"])
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

    if len(quiz["questions"]["L"]) >= int(os.environ["MAX_QUESTIONS"]):
        return {
            "message": "Max number of questions has been reached for this quiz."
        }, 422

    error_out = error.question_invalid(request.data)
    if error_out is not None:
        return error_out

    body = json.loads(request.data)
    question_id = str(uuid.uuid4())
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
        "is_multiple": { "BOOL": body["is_multiple"] },
        "choices": { "L": choices },
        "answers": { "NS": answers }
    })

    quiz["questions"]["L"].append({ "S": question_id })
    db.update_item(TableName="Quiz", Key={
        "quiz_id": { "S": quiz_id }
    }, AttributeUpdates={
        "questions": { "Value": quiz["questions"] }
    })

    return { "question_id": question_id }, 200
