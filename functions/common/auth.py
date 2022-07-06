import boto3

cognito = boto3.client("cognito-idp")

def get_user_id(event):
    return event.get("requestContext", {}).get("authorizer", {}) \
        .get("claims", {}).get("cognito:username", "empty")

def validate_user(token):
    try:
        user = cognito.get_user(AccessToken=token)
        return user["Username"], None
    except Exception as e:
        return None, ({ "message": "Invalid Access Token" }, 401)
