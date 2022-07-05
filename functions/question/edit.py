import boto3
import json
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
    error_out = error.quiz_not_creator(event, quiz)
    if error_out is not None:
        return error_out

    question_id = event["pathParameters"]["qid"]
    error_out = error.question_not_found(db, question_id)
    if error_out is not None:
        return error_out

    body = json.loads(event["body"])
    choices = []
    for choice in body["choices"]:
        choices.append({ "S": choice })

    error_out = error.answer_not_valid(choices, body["answers"])
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

    return {
        "statusCode": 200,
        "body": json.dumps({
            "question_id": question_id
        })
    }
