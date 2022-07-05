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


def quiz_not_creator(event, quiz):
    if auth.get_user_id(event) != quiz["user_id"]["S"]:
        return {
            "statusCode": 403,
            "body": json.dumps({
                "message": "The quiz does not belong to the user."
            })
        }

def quiz_title_empty(event):
    body = json.loads(event["body"])
    if len(body["title"]) < 1:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Quiz's title is empty."
            })
        }
