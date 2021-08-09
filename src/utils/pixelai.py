import os
import requests
import json

from extension import get_log_instance

log = get_log_instance(__name__)


def login():
    login_url = os.environ.get("URL") + "users/login"
    payload = {"username": os.environ.get(
        "PIXELAI_USERNAME"), "password": os.environ.get("PIXELAI_PASSWORD")}
    response = requests.request("POST", login_url, json=payload)
    try:
        response = json.loads(response.text)
        log.info(response)
        os.environ.update({"PIXELAI_ACCESS_TOKEN": response["access_token"]})
        headers = {
            'Authorization': 'Bearer ' + os.environ.get("PIXELAI_ACCESS_TOKEN")
        }
        return True, headers
    except Exception as err:
        log.error(err)
        return False, None
