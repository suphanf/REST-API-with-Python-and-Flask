import json
import common.auth as auth

def quiz_not_found(db, quiz_id):
    quiz = db.get_item(TableName="Quiz", Key={
        "quiz_id": { "S": quiz_id }
    }).get("Item")
    if quiz is None or quiz["is_disabled"]["BOOL"]:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "The quiz does not exist."
            })
        }

def quiz_not_published(event, quiz):
    if auth.get_user_id(event) != quiz["user_id"]["S"] and not quiz["is_published"]["BOOL"]:
         return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "The quiz does not exist."
            })
        }

def quiz_not_creator(event, quiz):
    if auth.get_user_id(event) != quiz["user_id"]["S"]:
        return {
            "statusCode": 403,
            "body": json.dumps({
                "message": "The quiz does not belong to the user."
            })
        }

def quiz_not_editable(quiz):
    if quiz["is_published"]["BOOL"]:
        return {
            "statusCode": 422,
            "body": json.dumps({
                "message": "The quiz cannot be edited because it is published."
            })
        }

def question_not_found(db, question_id):
    question = db.get_item(TableName="Question", Key={
        "question_id": { "S": question_id }
    }).get("Item")
    if question is None:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "The question does not exist."
            })
        }

def answer_not_valid(choices, answers, is_multiple):
    if not is_multiple and len(answers) > 1:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "A single-answer question must have one answer."
            })
        }
    for ans in answers:
        if not isinstance(ans, int) or ans < 0 or ans >= len(choices):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "An answer is not a valid integer [0 .. N(choices)-1]"
                })
            }

def submission_not_found(db, submission_id):
    submission = db.get_item(TableName="Submission", Key={
        "submission_id": { "S": submission_id }
    }).get("Item")
    if submission is None:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "The submission does not exist."
            })
        }

def submission_unauthorized(event, submission, quiz):
    user_id = auth.get_user_id(event)
    if user_id != submission["user_id"]["S"] and user_id != quiz["user_id"]["S"]:
        return {
            "statusCode": 403,
            "body": json.dumps({
                "message": "The user does not have permission to view this submission."
            })
        }

def submission_creator(event, quiz):
    if auth.get_user_id(event) == quiz["user_id"]["S"]:
        return {
            "statusCode": 403,
            "body": json.dumps({
                "message": "A user cannot take his/her own quiz."
            })
        }
