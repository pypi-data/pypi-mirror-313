import base64
import hashlib
import hmac
import json
import time
from urllib.parse import urlencode, urlparse

from ttxt_v2.core.web import BaseAuth, RESTRequest, WSRequest


class KucoinAuth(BaseAuth):
    """
    Authentication class for Kucoin API.
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        api_passphrase: str,
        api_key_version: str = "2",
    ):
        super().__init__()
        self.api_key = api_key
        self.secret_key = api_secret
        self.passphrase = api_passphrase
        self.api_key_version = api_key_version

    async def rest_authenticate(self, request: RESTRequest) -> RESTRequest:
        timestamp = str(int(time.time() * 1000))
        method = request.method.value.upper()
        parsed_url = urlparse(request.url)
        request_path = parsed_url.path

        if request.params:
            query_string = urlencode(request.params)
            request_path += f"?{query_string}"

        if not request.data:
            body = ""
            request.data = ""  # Ensure the request body is empty if there's no data

        str_to_sign = timestamp + method + request_path + request.data

        signature = base64.b64encode(
            hmac.new(
                self.secret_key.encode("utf-8"),
                str_to_sign.encode("utf-8"),
                hashlib.sha256,
            ).digest()
        ).decode("utf-8")

        # Encrypt passphrase for API key version 2 or 3
        if self.api_key_version in ["2", "3"]:
            passphrase = base64.b64encode(
                hmac.new(
                    self.secret_key.encode("utf-8"),
                    self.passphrase.encode("utf-8"),
                    hashlib.sha256,
                ).digest()
            ).decode("utf-8")
        else:
            passphrase = self.passphrase

        headers = request.headers or {}
        headers.update(
            {
                "KC-API-KEY": self.api_key,
                "KC-API-SIGN": signature,
                "KC-API-TIMESTAMP": timestamp,
                "KC-API-PASSPHRASE": passphrase,
                "KC-API-KEY-VERSION": self.api_key_version,
                "Content-Type": "application/json",
            }
        )
        request.headers = headers
        return request

    async def ws_authenticate(self, request: WSRequest) -> WSRequest:
        """
        For Kucoin, WebSocket authentication is handled via the token obtained from
        the bullet endpoint and included in the connection URL. No additional
        authentication is needed per request.
        """
        return request
