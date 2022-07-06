import json
import requests
from config import *

def get_http_auth_header(user_index=0):
    username_list = [USER01_USERNAME, USER02_USERNAME]
    password_list = [USER01_PASSWORD, USER02_PASSWORD]

    response = requests.post(f"{API_HOST}/users/auth", json={
        "auth_type": "USER_PASSWORD_AUTH",
        "username": username_list[user_index],
        "password": password_list[user_index]
    })

    return {
        "Authorization": json.loads(response.text)["id_token"]
    }
