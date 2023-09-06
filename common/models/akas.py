import base64
import hashlib
import hmac
import json
import secrets
import string
from django.db import models
from rest_framework.request import Request

access_key_length = 16
secret_access_key_length = 32


def generate_access_key():
    prefix = ""

    length = access_key_length - len(prefix)
    characters = string.ascii_letters + string.digits
    access_key = prefix + "".join(secrets.choice(characters) for _ in range(length))
    return access_key.lower()


def generate_secret_access_key():
    prefix = ""
    length = secret_access_key_length - len(prefix)
    characters = string.ascii_letters + string.digits + r"""#$&@"""
    secret_access_key = prefix + "".join(
        secrets.choice(characters) for _ in range(length)
    )
    return secret_access_key.lower()


class AccessKeyAndSecretModel(models.Model):
    key = models.CharField(max_length=access_key_length, default=generate_access_key)
    secret = models.CharField(
        max_length=secret_access_key_length, default=generate_secret_access_key
    )

    class Meta:
        verbose_name = "AccessKeySecret"
        verbose_name_plural = "AccessKeySecret"

    def __str__(self):
        return self.key

    def calculate_signature(self, request: Request):
        # Concatenate the request parameters and data into a single dictionary
        params = {}
        if request.query_params:
            params = request.query_params.dict()
        data = {}
        if request.data:
            data = request.data.dict()
        received_key, received_signature = request.headers.get(
            "Authorization", ""
        ).split(" ")

        request_data = {
            "key": received_key,
            "path": request._request.path,
            **params,
            **data,
        }
        sorted_request_data = {k: request_data[k] for k in sorted(request_data)}
        sorted_request_data_str = json.dumps(sorted_request_data)
        signature = hmac.new(
            self.secret.encode("utf-8"),
            sorted_request_data_str.encode("utf-8"),
            hashlib.sha256,
        ).digest()

        # Encode the signature in base64
        signature = base64.b64encode(signature).decode("utf-8")

        return f"{signature}"

    def verify_signature(self, reqeust: Request):
        request_headers = reqeust.headers
        _, received_signature = request_headers.get("Authorization", "").split(" ")
        expected_signature = self.calculate_signature(reqeust)
        return received_signature == expected_signature
