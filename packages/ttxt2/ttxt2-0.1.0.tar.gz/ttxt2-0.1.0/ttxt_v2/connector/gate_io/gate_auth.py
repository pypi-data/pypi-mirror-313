import hashlib
import hmac
import json
import time
from typing import Any, Mapping
from urllib.parse import urlencode, urlparse

from ttxt_v2.core.web import BaseAuth, RESTRequest, WSJSONRequest, WSRequest


class GateAuth(BaseAuth):
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
        """
        Authenticates the REST request by adding the required headers.

        Args:
            request (RESTRequest): The REST request to authenticate.

        Returns:
            RESTRequest: The authenticated REST request.
        """
        # Get current timestamp as a string
        timestamp = str(int(time.time()))
        # Get the HTTP method in uppercase
        method = request.method.value.upper()
        # Parse the URL to extract the path and query
        parsed_url = urlparse(request.url)
        request_url = parsed_url.path  # Request URL without the base URL
        # Construct the query string from request.params
        if request.params:
            # Ensure the parameters are sorted
            sorted_params = sorted(request.params.items())
            query_string = urlencode(sorted_params)
        else:
            query_string = ""

        # Prepare the request payload (body)
        if request.data:
            # Ensure the payload is JSON serialized with separators
            payload_json = json.dumps(request.data, separators=(",", ":"))
            # Calculate the SHA512 hash of the payload
            sha512 = hashlib.sha512()
            sha512.update(payload_json.encode("utf-8"))
            hashed_payload = sha512.hexdigest()
        else:
            # If there's no payload, hash of empty string
            hashed_payload = hashlib.sha512("".encode("utf-8")).hexdigest()

        signature_string = (
            f"{method}\n{request_url}\n{query_string}\n{hashed_payload}\n{timestamp}"
        )

        # Calculate the HMAC SHA512 of the signature string
        sign = hmac.new(
            self.secret_key.encode("utf-8"),
            signature_string.encode("utf-8"),
            digestmod=hashlib.sha512,
        ).hexdigest()

        # Set the required headers
        request.headers["KEY"] = self.api_key
        request.headers["Timestamp"] = timestamp
        request.headers["SIGN"] = sign

        return request

    async def ws_authenticate(self, request: WSRequest) -> WSRequest:
        """
        Authenticates the WebSocket request by adding the authentication message.

        Args:
            request (WSRequest): The WebSocket request to authenticate.

        Returns:
            WSRequest: The authenticated WebSocket request.
        """
        if not isinstance(request, WSJSONRequest):
            raise RuntimeError("Only JSON requests are supported")
        request.payload["auth"] = self._generate_ws_signature(
            request.payload["channel"],
            request.payload["event"],
            request.payload["time"],
        )
        return request

    def _generate_ws_signature(
        self, channel: str, event: str, timestamp: int
    ) -> Mapping[str, Any]:
        s = f"channel={channel}&event={event}&time={timestamp}"
        sign = hmac.new(
            self.secret_key.encode("utf-8"), s.encode("utf-8"), digestmod="sha512"
        ).hexdigest()
        return {"method": "api_key", "KEY": self.api_key, "SIGN": sign}

    def generate_ws_auth_message(self) -> dict:
        return NotImplemented

    def _time(self) -> float:
        """
        Gets the current time in seconds since the epoch.

        Returns:
            float: The current time in seconds.
        """
        return time.time()
