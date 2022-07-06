import json
import requests
from config import *

def get_http_auth_header():
    response = requests.post(f"{API_HOST}/users/auth", json={
        "auth_type": "USER_PASSWORD_AUTH",
        "username": USER01_USERNAME,
        "password": USER01_PASSWORD
    })

    return {
        "Authorization": json.loads(response.text)["id_token"]
    }
