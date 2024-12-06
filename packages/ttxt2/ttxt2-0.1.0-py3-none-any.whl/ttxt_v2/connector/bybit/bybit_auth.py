import hmac
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

from ttxt_v2.core.web import BaseAuth, RESTRequest, WSJSONRequest, WSRequest
from ttxt_v2.core.web.data_types import RESTMethod


class BybitAuth(BaseAuth):
    """
    Authentication class for Bybit WebSocket API.

    Attributes:
        api_key (str): The API key for authentication.
        secret_key (str): The secret key for authentication.
    """

    def __init__(self, api_key: str, api_secret: str):
        """
        Initializes the BybitAuth with the given API key and secret.

        Args:
            api_key (str): The API key for authentication.
            api_secret (str): The secret key for authentication.
        """
        super().__init__()
        self.api_key = api_key
        self.secret_key = api_secret

    async def rest_authenticate(self, request: RESTRequest) -> RESTRequest:
        return self.add_auth_headers(method=request.method, request=request)

    def add_auth_headers(self, method: RESTMethod, request: Optional[Dict[str, Any]]):
        ts = str(int(time.time() * 10**3))
        headers = {}
        headers["X-BAPI-TIMESTAMP"] = str(ts)
        headers["X-BAPI-API-KEY"] = self.api_key
        if method == RESTMethod.POST:
            signature = self._generate_rest_signature(
                timestamp=ts, method=method, payload=request.data
            )
        else:
            signature = self._generate_rest_signature(
                timestamp=ts, method=method, payload=request.params
            )

        headers["X-BAPI-SIGN"] = signature
        headers["X-BAPI-RECV-WINDOW"] = "8000"
        request.headers = (
            {**request.headers, **headers} if request.headers is not None else headers
        )
        return request

    def _generate_rest_signature(
        self, timestamp: str, method: RESTMethod, payload: Optional[Dict[str, Any]]
    ) -> str:
        param_str = ""
        if payload is None:
            payload = {}
        if method == RESTMethod.GET:
            param_str = timestamp + self.api_key + "8000" + urlencode(payload)
        elif method == RESTMethod.POST:
            param_str = timestamp + self.api_key + "8000" + f"{payload}"
        signature = hmac.new(
            bytes(self.secret_key, "utf-8"),
            param_str.encode("utf-8"),
            digestmod="sha256",
        ).hexdigest()
        return signature

    async def ws_authenticate(self, request: WSRequest) -> WSRequest:
        """
        Authenticates the WebSocket request by adding the authentication message.

        Args:
            request (WSRequest): The WebSocket request to authenticate.

        Returns:
            WSRequest: The authenticated WebSocket request.
        """
        return WSJSONRequest(payload=self.generate_ws_auth_message())

    def _generate_ws_signature(self, expires: int) -> str:
        """
        Generates the WebSocket signature for authentication.

        Args:
            expires (int): The expiration time in milliseconds.

        Returns:
            str: The generated WebSocket signature.
        """
        signature = str(
            hmac.new(
                bytes(self.secret_key, "utf-8"),
                bytes(f"GET/realtime{expires}", "utf-8"),
                digestmod="sha256",
            ).hexdigest()
        )
        return signature

    def generate_ws_auth_message(self) -> dict:
        """
        Generates the authentication message to start receiving messages from
        the private WebSocket channels.

        Returns:
            dict: The authentication message.
        """
        expires = int((self._time() + 10000) * 1000)
        signature = self._generate_ws_signature(expires)
        auth_message = {"op": "auth", "args": [self.api_key, expires, signature]}
        return auth_message

    def _time(self) -> float:
        """
        Gets the current time in seconds since the epoch.

        Returns:
            float: The current time in seconds.
        """
        return time.time()
