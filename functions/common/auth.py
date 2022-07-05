def get_user_id(event):
    return event.get("requestContext", {}).get("authorizer", {}) \
        .get("claims", {}).get("cognito:username", "empty")
