import boto3
import datetime
import json
import uuid
import functions.common.auth as auth
import functions.common.error as error
import functions.common.util as util
from flask import Blueprint, request

cognito = boto3.client("cognito-idp")
db = boto3.client("dynamodb")
submission_create_file = Blueprint("submission_create_file", __name__)

@submission_create_file.route("/quizzes/<quiz_id>/submissions", methods=["POST"])
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
    error_out = error.submission_creator(user_id, quiz)
    if error_out is not None:
        return error_out

    error_out = error.quiz_not_published(user_id, quiz)
    if error_out is not None:
        return error_out

    results = db.query(TableName="Submission",
        IndexName="user_id-quiz_id-index",
        KeyConditionExpression="user_id = :user_id AND quiz_id = :quiz_id",
        ExpressionAttributeValues={
            ":user_id": { "S": user_id },
            ":quiz_id": { "S": quiz_id }
        }
    )
    if len(results["Items"]) > 0:
        return { "message": "The quiz has already been taken by this user." }, 403

    body = json.loads(request.data)
    if len(body) != len(quiz["questions"]["L"]):
        return { "message": "A submission must have answers (or skip) for all questions." }, 400

    question_map = util.get_question_map(db, quiz_id)
    questions = []
    for question_id in map(lambda x: x["S"], quiz["questions"]["L"]):
        questions.append(question_map[question_id])

    total_score = 0
    user_answers = []
    for question, answers in zip(questions, body):
        if len(answers) == 0:
            user_answers.append({
                "M": {
                    "score": { "N": "0" }
                }
            })
            continue
        error_out = error.answer_not_valid(question["choices"], answers, question["is_multiple"])
        if error_out is not None:
            return error_out
        
        score = 0
        for ans in answers:
            if ans in question["answers"]:
                score += 1 / len(question["answers"])
            else:
                score -= 1 / (len(question["choices"]) - len(question["answers"]))
        total_score += score
        user_answers.append({
            "M": {
                "chosen": { "NS": list(map(str, answers)) },
                "score": { "N": "{:.2f}".format(score) }
            }
        })

    dt_str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    submission_id = str(uuid.uuid4())
    db.put_item(TableName="Submission", Item={
        "submission_id": { "S": submission_id },
        "quiz_id": { "S": quiz_id },
        "quiz_title": quiz["title"],
        "user_id": { "S": user_id },
        "timestamp": { "S": dt_str },
        "total_score": { "N": "{:.2f}".format(total_score) },
        "user_answers": { "L": user_answers }
    })

    return { "submission_id": submission_id }, 200
