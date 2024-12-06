import hashlib
import hmac
import time
import urllib.parse

from ttxt_v2.core.web import BaseAuth
from ttxt_v2.core.web.data_types import RESTMethod, RESTRequest, WSRequest
from ttxt_v2.utils.logger import logger


class BinanceAuth(BaseAuth):
    def __init__(self, api_key: str, api_secret: str):
        super().__init__()
        self._api_key = api_key
        self._api_secret = api_secret

    async def rest_authenticate(self, request: RESTRequest) -> RESTRequest:
        if request.headers is None:
            request.headers = {}
        request.headers["X-MBX-APIKEY"] = self._api_key

        timestamp = int(time.time() * 1000)
        if request.method == RESTMethod.GET:
            params = request.params or {}
            params["timestamp"] = timestamp
            query_string = urllib.parse.urlencode(params)
            signature = hmac.new(
                self._api_secret.encode("utf-8"),
                query_string.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            params["signature"] = signature
            request.params = params
        else:
            data = request.data or {}
            data["timestamp"] = timestamp
            query_string = urllib.parse.urlencode(data)
            signature = hmac.new(
                self._api_secret.encode("utf-8"),
                query_string.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            data["signature"] = signature
            request.data = data

        return request

    async def ws_authenticate(self, request: WSRequest) -> WSRequest:
        """
        Adds authentication to a WebSocket request.
        """
        params = request.payload.get("params", {})
        params["apiKey"] = self._api_key
        timestamp = int(time.time() * 1000)
        params["timestamp"] = timestamp
        recv_window = 5000  # Optional, adjust as needed
        params["recvWindow"] = recv_window
        # Generate the query string in order of sorted parameters
        query_string = "&".join([f"{key}={params[key]}" for key in sorted(params)])
        signature = hmac.new(
            self._api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        request.payload["params"] = params

        logger.debug(f"Authenticated req: {request}")
        return request
