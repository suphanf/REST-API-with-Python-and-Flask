import boto3
import functions.common.auth as auth
import functions.common.error as error
import functions.common.util as util
from flask import Blueprint, request

cognito = boto3.client("cognito-idp")
db = boto3.client("dynamodb")
quiz_get_file = Blueprint("quiz_get_file", __name__)

@quiz_get_file.route("/quizzes/<quiz_id>", methods=["GET"])
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

    error_out = error.quiz_not_published(user_id, quiz)
    if error_out is not None:
        return error_out

    question_map = util.get_question_map(db, quiz_id)
    questions = []
    for question_id in map(lambda x: x["S"], quiz["questions"]["L"]):
        question = question_map[question_id]
        if user_id != quiz["user_id"]["S"]:
            del question["answers"]
        questions.append(question)

    return {
        "title": quiz["title"]["S"],
        "timestamp": quiz["timestamp"]["S"],
        "questions": questions,
        "is_published": quiz["is_published"]["BOOL"]
    }, 200
