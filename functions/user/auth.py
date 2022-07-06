import boto3
import json
import os
from flask import Blueprint, request

cognito = boto3.client("cognito-idp")
db = boto3.client("dynamodb")
user_auth_file = Blueprint("user_auth_file", __name__)

@user_auth_file.route("/users/auth", methods=["POST"])
def lambda_handler():
    body = json.loads(request.data)

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
            "access_token": response["AuthenticationResult"]["AccessToken"],
            "refresh_token": response["AuthenticationResult"]["RefreshToken"]
        }, 200
    elif body["auth_type"] == "REFRESH_TOKEN":
        response = cognito.initiate_auth(
            ClientId=os.environ["CLIENT_ID"],
            AuthFlow=body["auth_type"],
            AuthParameters={
                "REFRESH_TOKEN": body["refresh_token"]
            }
        )
        return {
            "id_token": response["AuthenticationResult"]["IdToken"],
            "refresh_token": body["refresh_token"]
        }, 200
    else:
        return { "message": "Unknown authentication type" }, 400
