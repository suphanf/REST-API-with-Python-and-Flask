import boto3
import json
import os

cognito = boto3.client("cognito-idp")

def lambda_handler(event, context):
    body = json.loads(event["body"])

    response = cognito.sign_up(
        ClientId=os.environ["CLIENT_ID"],
        Username=body["username"],
        Password=body["password"]
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "user_id": response["UserSub"]
        })
    }
