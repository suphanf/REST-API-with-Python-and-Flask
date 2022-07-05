import json
import common.auth as auth

def quiz_id_missing(event):
    if event.get("pathParameters") is not None:
        if event["pathParameters"].get("id") is not None:
            return None

    return {
        "statusCode": 400,
        "body": json.dumps({
            "message": "Quiz ID is missing."
        })
    }


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


def quiz_title_missing(event):
    if event.get("body") is not None:
        try:
            body = json.loads(event["body"])
        except json.decoder.JSONDecodeError:
            body = {}
        if len(body.get("title", "")) > 0:
            return None

    return {
        "statusCode": 400,
        "body": json.dumps({
            "message": "Title is missing or empty."
        })
    }
