import secrets
import time
from typing import Optional
from urllib.parse import urlparse

import jwt
from cryptography.hazmat.primitives import serialization

from ttxt_v2.core.web import BaseAuth, RESTRequest, WSRequest
from ttxt_v2.utils.logger import logger


class CoinbaseAuth(BaseAuth):
    """
    Authentication class for Coinbase API.
    """

    def __init__(self, api_key: str, api_secret: str):
        super().__init__()
        self.api_key = (
            api_key  # key name, e.g., 'organizations/{org_id}/apiKeys/{key_id}'
        )
        self.secret_key = api_secret  # PEM-formatted private key
        # Replace literal '\n' with actual newlines
        self.secret_key = self.secret_key.replace("\\n", "\n").strip()

        private_key_bytes = self.secret_key.encode("utf-8")
        self.private_key = serialization.load_pem_private_key(
            private_key_bytes, password=None
        )
        self._cached_jwt = None
        self._jwt_expiry = 0

    def _generate_jwt(self, uri: Optional[str] = None) -> str:
        current_time = int(time.time())
        payload = {
            "sub": self.api_key,
            "iss": "cdp",
            "nbf": current_time,
            "exp": current_time + 120,  # JWT valid for 2 minutes
        }
        if uri:
            payload["uri"] = uri
        headers = {
            "kid": self.api_key,
            "nonce": secrets.token_hex(),
        }
        jwt_token = jwt.encode(
            payload,
            self.private_key,
            algorithm="ES256",
            headers=headers,
        )
        return jwt_token

    def _get_cached_jwt(self, uri: Optional[str] = None) -> str:
        current_time = int(time.time())
        # Check if JWT is still valid
        if self._cached_jwt and current_time < self._jwt_expiry:
            return self._cached_jwt
        else:
            # Generate new JWT
            jwt_token = self._generate_jwt(uri)
            self._cached_jwt = jwt_token
            self._jwt_expiry = current_time + 120  # Update expiry time
            return jwt_token

    async def rest_authenticate(self, request: RESTRequest) -> RESTRequest:
        """
        Coinbase REST API requires JWT authentication.
        """
        # Extract method, host, and path
        method = request.method.value.upper()
        parsed_url = urlparse(request.url)
        host = parsed_url.netloc
        path = parsed_url.path

        uri = f"{method} {host}{path}"
        jwt_token = self._get_cached_jwt(uri)

        if request.headers is None:
            request.headers = {}
        request.headers["Authorization"] = f"Bearer {jwt_token}"
        return request

    async def ws_authenticate(self, request: WSRequest) -> WSRequest:
        """
        Coinbase requires a JWT to be included in the WebSocket request payload.
        """
        jwt_token = self._get_cached_jwt()
        request.payload["jwt"] = jwt_token
        return request
