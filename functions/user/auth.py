import boto3
import json
import os

cognito = boto3.client("cognito-idp")

def lambda_handler(event, context):
    body = json.loads(event["body"])

    if body["auth_type"] == "USER_PASSWORD_AUTH":
        response = cognito.initiate_auth(
            ClientId=os.environ["CLIENT_ID"],
            AuthFlow=body["auth_type"],
            AuthParameters={
                "USERNAME": body["username"],
                "PASSWORD": body["password"]
            }
        )
        return {
            "statusCode": 200,
            "body": json.dumps({
                "id_token": response["AuthenticationResult"]["IdToken"],
                "refresh_token": response["AuthenticationResult"]["RefreshToken"]
            })
        }
    elif body["auth_type"] == "REFRESH_TOKEN":
        response = cognito.initiate_auth(
            ClientId=os.environ["CLIENT_ID"],
            AuthFlow=body["auth_type"],
            AuthParameters={
                "REFRESH_TOKEN": body["refresh_token"]
            }
        )
        return {
            "statusCode": 200,
            "body": json.dumps({
                "id_token": response["AuthenticationResult"]["IdToken"],
                "refresh_token": body["refresh_token"]
            })
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Unknown authentication type"
            })
        }
