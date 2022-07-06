import json
import os
import functions.common.auth as auth

def title_empty(data):
    try:
        body = json.loads(data)
    except ValueError:
        body = {}
    if len(body.get("title", "")) == 0:
        return { "message": "Quiz's title cannot be empty" }, 400

def quiz_not_found(db, quiz_id):
    quiz = db.get_item(TableName="Quiz", Key={
        "quiz_id": { "S": quiz_id }
    }).get("Item")
    if quiz is None or quiz["is_disabled"]["BOOL"]:
        return { "message": "The quiz does not exist." }, 404

def quiz_not_published(user_id, quiz):
    if user_id != quiz["user_id"]["S"] and not quiz["is_published"]["BOOL"]:
         return { "message": "The quiz does not exist." }, 404

def quiz_not_creator(user_id, quiz):
    if user_id != quiz["user_id"]["S"]:
        return { "message": "The quiz does not belong to the user." }, 403

def quiz_not_editable(quiz):
    if quiz["is_published"]["BOOL"]:
        return { "message": "The quiz cannot be edited because it is published." }, 422

def question_not_found(db, question_id):
    question = db.get_item(TableName="Question", Key={
        "question_id": { "S": question_id }
    }).get("Item")
    if question is None:
        return { "message": "The question does not exist." }, 404

def question_invalid(data):
    try:
        body = json.loads(data)
    except ValueError:
        body = {}
    text = body.get("text", "")
    is_multiple = body.get("is_multiple")
    choices = body.get("choices", [])
    answers = body.get("answers", [])
    if len(body.get("text", "")) == 0 or not isinstance(body.get("is_multiple"), bool) or \
        len(choices) < int(os.environ["MIN_CHOICES"]) or \
        len(choices) > int(os.environ["MAX_CHOICES"]) or \
        len(answers) < int(os.environ["MIN_ANSWERS"]) or \
        len(answers) > int(os.environ["MAX_ANSWERS"]):
        return { "message": "Question format is invalid" }, 400

def answer_not_valid(choices, answers, is_multiple):
    if not is_multiple and len(answers) > 1:
        return {
             "message": "A single-answer question must have one answer."
        }, 400
    for ans in answers:
        if not isinstance(ans, int) or ans < 0 or ans >= len(choices):
            return {
                "message": "An answer is not a valid integer [0 .. N(choices)-1]"
            }, 400

def submission_not_found(db, submission_id):
    submission = db.get_item(TableName="Submission", Key={
        "submission_id": { "S": submission_id }
    }).get("Item")
    if submission is None:
        return { "message": "The submission does not exist." }, 404

def submission_unauthorized(user_id, submission, quiz):
    if user_id != submission["user_id"]["S"] and user_id != quiz["user_id"]["S"]:
        return { "message": "The user does not have permission to view this submission." }, 403

def submission_creator(user_id, quiz):
    if user_id == quiz["user_id"]["S"]:
        return { "message": "A user cannot take his/her own quiz." }, 403
