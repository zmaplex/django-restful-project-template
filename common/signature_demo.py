import base64
import hashlib
import hmac
import json

import requests

host = "http://127.0.0.1:8000"

api = "/api/user/ping_with_aceess_key/"

access_key = "wprqvzcrl1rymjnv"
access_secret = "9xx6l0hil@l@10$sttttcef1@tenkfia"


def calculate_signature(access_key, access_secret, path, params, data):
    _ready_data = {"key": access_key, "path": path, **params, **data}
    sorted_request_data = {k: _ready_data[k] for k in sorted(_ready_data)}
    sorted_request_data_str = json.dumps(sorted_request_data)
    print(sorted_request_data_str)
    signature = hmac.new(
        access_secret.encode("utf-8"),
        sorted_request_data_str.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    signature = base64.b64encode(signature).decode("utf-8")
    return f"{signature}"


params = {"domain": "domain.com"}
data = {"action": "get"}

headers = {
    "Authorization": f"{access_key} {calculate_signature(access_key, access_secret, api, params, data)}"
}

res = requests.get(
    host + api,
    params=params,
    data=data,
    headers=headers,
)

print(headers)
print(res.text)
