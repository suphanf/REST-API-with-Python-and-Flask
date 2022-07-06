import boto3
import json
import os
from flask import Blueprint, request

cognito = boto3.client("cognito-idp")
db = boto3.client("dynamodb")
user_signup_file = Blueprint("user_signup_file", __name__)

@user_signup_file.route("/users/signup", methods=["POST"])
def lambda_handler():
    body = json.loads(request.data)

    response = cognito.sign_up(
        ClientId=os.environ["CLIENT_ID"],
        Username=body["username"],
        Password=body["password"]
    )

    return { "user_id": response["UserSub"] }, 200
