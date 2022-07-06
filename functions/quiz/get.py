import boto3
import json
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

    error_out = error.quiz_not_published(event, quiz)
    if error_out is not None:
        return error_out

    question_map = util.get_question_map(db, quiz_id)
    this_user_id = auth.get_user_id(event)
    questions = []
    for question_id in map(lambda x: x["S"], quiz["questions"]["L"]):
        question = question_map[question_id]
        if this_user_id != quiz["user_id"]["S"]:
            del question["answers"]
        questions.append(question)

    return {
      "statusCode": 200,
      "body": json.dumps({
          "title": quiz["title"]["S"],
          "timestamp": quiz["timestamp"]["S"],
          "questions": questions,
          "is_published": quiz["is_published"]["BOOL"]
      })
    }
