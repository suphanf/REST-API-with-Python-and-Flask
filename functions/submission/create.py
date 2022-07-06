import boto3
import datetime
import json
import uuid
import common.auth as auth
import common.error as error
import common.util as util

db = boto3.client("dynamodb")

def lambda_handler(event, context):
    quiz_id = event["pathParameters"]["id"]
    error_out = error.quiz_not_found(db, quiz_id)
    if error_out is not None:
        return error_out

    quiz = db.get_item(TableName="Quiz", Key={
        "quiz_id": { "S": quiz_id }
    }).get("Item")
    error_out = error.submission_creator(event, quiz)
    if error_out is not None:
        return error_out

    error_out = error.quiz_not_published(event, quiz)
    if error_out is not None:
        return error_out

    results = db.query(TableName="Submission",
        IndexName="user_id-quiz_id-index",
        KeyConditionExpression="user_id = :user_id AND quiz_id = :quiz_id",
        ExpressionAttributeValues={
            ":user_id": { "S": auth.get_user_id(event) },
            ":quiz_id": { "S": quiz_id }
        }
    )
    if len(results["Items"]) > 0:
        return {
            "statusCode": 403,
            "body": json.dumps({
                "message": "The quiz has already been taken by this user."
            })
        }

    body = json.loads(event["body"])
    if len(body) != len(quiz["questions"]["L"]):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "A submission must have answers (or skip) for all questions."
            })
        }

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
        "user_id": { "S": auth.get_user_id(event) },
        "timestamp": { "S": dt_str },
        "total_score": { "N": "{:.2f}".format(total_score) },
        "user_answers": { "L": user_answers }
    })

    return {
        "statusCode": 200,
        "body": json.dumps({
            "submission_id": submission_id
        })
    }
