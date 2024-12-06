import base64
import hashlib
import hmac
import time
from typing import Any, Mapping, Tuple
from urllib.parse import urlparse

from ttxt_v2.core.web import BaseAuth, RESTRequest, WSJSONRequest, WSRequest
from ttxt_v2.utils.logger import logger


class BitgetAuth(BaseAuth):
    """
    Authentication class for Bybit WebSocket API.

    Attributes:
        api_key (str): The API key for authentication.
        secret_key (str): The secret key for authentication.
    """

    def __init__(self, api_key: str, api_secret: str, api_passphrase: str):
        """
        Initializes the BybitAuth with the given API key and secret.

        Args:
            api_key (str): The API key for authentication.
            api_secret (str): The secret key for authentication.
        """
        super().__init__()
        self.api_key = api_key
        self.secret_key = api_secret
        self.passphrase = api_passphrase

    async def rest_authenticate(self, request: RESTRequest) -> RESTRequest:
        timestamp = str(int(time.time() * 1000))  # Milliseconds since Epoch
        method_str = request.method.value.upper()

        # Build request path and query string
        request_path = urlparse(request.url).path

        def parse_params_to_str(params):
            params = [(key, val) for key, val in params.items()]
            params.sort(key=lambda x: x[0])
            url = "?" + to_query(params)
            if url == "?":
                return ""
            return url

        def to_query(params):
            url = ""
            for key, value in params:
                url = url + str(key) + "=" + str(value) + "&"
            return url[0:-1]

        # Prepare body
        body = ""
        if method_str in ["POST", "PUT"]:
            if request.data:
                body = str(request.data)
            else:
                body = ""

        # Concatenate the string to sign
        if request.params:
            sign_content = (
                timestamp
                + method_str
                + str(request_path)
                + "?"
                + parse_params_to_str(request.params)
                + body
            )
        else:
            sign_content = timestamp + method_str + str(request_path) + body

        # Generate signature
        signature = base64.b64encode(
            hmac.new(
                self.secret_key.encode("utf-8"),
                sign_content.encode("utf-8"),
                hashlib.sha256,
            ).digest()
        ).decode()

        # Set headers
        headers = request.headers or {}
        headers.update(
            {
                "ACCESS-KEY": self.api_key,
                "ACCESS-SIGN": signature,
                "ACCESS-TIMESTAMP": timestamp,
                "ACCESS-PASSPHRASE": self.passphrase,
                "locale": "en-US",  # Set your desired locale
            }
        )

        request.headers = headers
        return request

    async def ws_authenticate(self, request: WSRequest) -> WSRequest:
        """
        Authenticates the WebSocket request by adding the authentication message.

        Args:
            request (WSRequest): The WebSocket request to authenticate.

        Returns:
            WSRequest: The authenticated WebSocket request.
        """
        return WSJSONRequest(payload=self.generate_ws_auth_message())

    def _generate_ws_signature(self) -> Tuple[str, str]:
        """
        Generates the WebSocket signature for authentication.

        Args:
            expires (int): The expiration time in milliseconds.

        Returns:
            str: The generated WebSocket signature.
        """
        ts = str(int(time.time()))
        conc_str = f"{ts}GET/user/verify"
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            conc_str.encode("utf-8"),
            hashlib.sha256,
        ).digest()

        encoded = base64.b64encode(signature).decode()

        return ts, encoded

    def generate_ws_auth_message(self) -> Mapping[str, Any]:
        """
        Generates the authentication message to start receiving messages from
        the private WebSocket channels.

        Returns:
            dict: The authentication message.
        """

        ts, sign = self._generate_ws_signature()
        auth_msg = {
            "op": "login",
            "args": [
                {
                    "apiKey": self.api_key,
                    "passphrase": self.passphrase,
                    "timestamp": ts,
                    "sign": sign,
                }
            ],
        }
        return auth_msg
