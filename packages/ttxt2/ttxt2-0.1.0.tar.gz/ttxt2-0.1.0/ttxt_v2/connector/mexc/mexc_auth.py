import hashlib
import hmac
import json
import time
import urllib.parse
from typing import Any, Dict

from ttxt_v2.core.web import BaseAuth, RESTRequest, WSRequest
from ttxt_v2.core.web.data_types import RESTMethod
from ttxt_v2.utils.logger import logger


class MexcAuth(BaseAuth):
    def __init__(self, api_key: str, api_secret: str):
        super().__init__()
        self.api_key = api_key
        self.secret_key = api_secret

    async def rest_authenticate(self, request: RESTRequest) -> RESTRequest:
        if request.headers is None:
            request.headers = {}

        request.headers["X-MEXC-APIKEY"] = self.api_key
        request.headers["Content-Type"] = "application/json"

        timestamp = int(time.time() * 1000)

        if request.method == RESTMethod.GET:
            params = request.params or {}
            params["timestamp"] = timestamp

            total_params = self._build_total_params(params, {})
            signature = self._generate_rest_signature(total_params)
            params["signature"] = signature
            request.params = params

        else:
            params = request.params or {}
            if request.data:
                data = json.loads(request.data)
            else:
                data = {}
            data["timestamp"] = timestamp

            total_params = self._build_total_params(params, data)
            signature = self._generate_rest_signature(total_params)
            data["signature"] = signature

            request.data = data

        return request

    def _generate_rest_signature(self, total_params: str) -> str:
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            total_params.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return signature

    def _build_total_params(self, params: Dict[str, Any], data: Dict[str, Any]) -> str:
        params_encoded = "&".join(
            f"{urllib.parse.quote(str(k), safe='')}={urllib.parse.quote(str(v), safe='')}"
            for k, v in params.items()
        )
        data_encoded = "&".join(
            f"{urllib.parse.quote(str(k), safe='')}={urllib.parse.quote(str(v), safe='')}"
            for k, v in data.items()
        )
        total_params = "&".join(filter(None, [params_encoded, data_encoded]))
        return total_params

    async def ws_authenticate(self, request: WSRequest) -> WSRequest:
        """
        MEXC does not require WebSocket authentication for public data.

        Args:
            request (WSRequest): The WebSocket request.

        Returns:
            WSRequest: The unchanged WebSocket request.
        """
        return request
