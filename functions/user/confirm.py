import boto3
import json
import os
from flask import Blueprint, request

cognito = boto3.client("cognito-idp")
db = boto3.client("dynamodb")
user_confirm_file = Blueprint("user_confirm_file", __name__)

@user_confirm_file.route("/users/confirm", methods=["POST"])
def lambda_handler():
    body = json.loads(request.data)

    response = cognito.confirm_sign_up(
        ClientId=os.environ["CLIENT_ID"],
        Username=body["username"],
        ConfirmationCode=body["confirmation_code"]
    )

    return { "sucesss": True }, 200
