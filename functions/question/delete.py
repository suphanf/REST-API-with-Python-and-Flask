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

    error_out = error.quiz_not_editable(quiz)
    if error_out is not None:
        return error_out

    question_id = event["pathParameters"]["qid"]
    error_out = error.question_not_found(db, question_id)
    if error_out is not None:
        return error_out

    quiz["questions"]["L"].remove({ "S": question_id })
    db.update_item(TableName="Quiz", Key={
        "quiz_id": { "S": quiz_id }
    }, AttributeUpdates={
        "questions": { "Value": quiz["questions"] }
    })

    db.delete_item(TableName="Question", Key={
        "question_id": { "S": question_id }
    })

    return {
        "statusCode": 200,
        "body": json.dumps({
            "question_id": question_id
        })
    }
