import boto3
import json
import common.error as error

db = boto3.client("dynamodb")

def lambda_handler(event, context):
    submission_id = event["pathParameters"]["id"]
    error_out = error.submission_not_found(db, submission_id)
    if error_out is not None:
        return error_out

    submission = db.get_item(TableName="Submission", Key={
        "submission_id": { "S": submission_id }
    }).get("Item")

    quiz = db.get_item(TableName="Quiz", Key={
        "quiz_id": submission["quiz_id"]
    }).get("Item")

    error_out = error.submission_unauthorized(event, submission, quiz)
    if error_out is not None:
        return error_out

    results = db.query(TableName="Question",
        IndexName="quiz_id-index",
        KeyConditionExpression="quiz_id = :quiz_id",
        ExpressionAttributeValues={
            ":quiz_id": submission["quiz_id"]
        }
    )
    questions = []
    for result in results["Items"]:
        questions.append({
            "text": result["text"]["S"],
            "choices": list(map(lambda x: x["S"], result["choices"]["L"]))
        })

    user_answers = []
    for question, u_answer in zip(questions, submission["user_answers"]["L"]):
        chosen_index = sorted(list(map(int, u_answer["M"].get("chosen", {}).get("NS", []))))
        chosen_text = list(map(lambda x: question["choices"][x], chosen_index))
        user_answers.append({
            "question_text": question["text"],
            "chosen": chosen_text,
            "score": u_answer["M"]["score"]["N"]
        })

    return {
        "statusCode": 200,
        "body": json.dumps({
            "quiz_title": submission["quiz_title"]["S"],
            "user_id": submission["user_id"]["S"],
            "timestamp": submission["timestamp"]["S"],
            "total_score": submission["total_score"]["N"],
            "user_answers": user_answers
        })
    }
