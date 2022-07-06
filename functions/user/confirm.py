import boto3
import json
import os

cognito = boto3.client("cognito-idp")

def lambda_handler(event, context):
    body = json.loads(event["body"])

    response = cognito.confirm_sign_up(
        ClientId=os.environ["CLIENT_ID"],
        Username=body["username"],
        ConfirmationCode=body["confirmation_code"]
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "sucesss": True
        })
    }
