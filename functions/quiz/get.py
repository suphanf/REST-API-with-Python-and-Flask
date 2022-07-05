import boto3
import json
import common.auth as auth
import common.error as error

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

    results = db.query(TableName="Question",
        IndexName="quiz_id-index",
        KeyConditionExpression="quiz_id = :quiz_id",
        ExpressionAttributeValues={
            ":quiz_id": { "S": quiz_id }
        }
    )

    this_user_id = auth.get_user_id(event)
    questions = []
    for result in results["Items"]:
        question = {
            "question_id": result["question_id"]["S"],
            "text": result["text"]["S"],
            "is_multiple": result["is_multiple"]["BOOL"],
            "choices": list(map(lambda x: x["S"], result["choices"]["L"]))
        }
        if this_user_id == quiz["user_id"]["S"]:
            question["answers"] = list(map(int, result["answers"]["NS"]))
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
