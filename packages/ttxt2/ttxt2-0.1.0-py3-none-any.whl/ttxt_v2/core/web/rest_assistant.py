import json
from copy import deepcopy
from typing import Any, Dict, Optional, Union

from .base_auth import BaseAuth
from .data_types import RESTMethod, RESTRequest, RESTResponse
from .rest_connection import RESTConnection


class RESTAssistant:
    def __init__(self, connection: RESTConnection, auth: Optional[BaseAuth] = None):
        self._connection = connection
        self._auth = auth

    async def execute_request(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        method: RESTMethod = RESTMethod.GET,
        is_auth_required: bool = False,
        ret_err: bool = False,
        timeout: Optional[float] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> Union[str, Dict[str, Any]]:
        response = await self.execute_request_and_get_response(
            url=url,
            params=params,
            data=data,
            method=method,
            is_auth_required=is_auth_required,
            ret_err=ret_err,
            timeout=timeout,
            headers=headers,
        )

        response_json = await response.json()
        return response_json

    async def execute_request_and_get_response(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        method: RESTMethod = RESTMethod.GET,
        is_auth_required: bool = False,
        ret_err: bool = False,
        timeout: Optional[float] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> RESTResponse:
        headers = headers or {}
        local_headers = deepcopy(headers)
        """
        local_headers = {
            "Content-Type": (
                "application/json"
                if method != RESTMethod.GET
                else "application/x-www-form-urlencoded"
            )
        }
        """
        # Only set Content-Type for methods other than GET
        if method != RESTMethod.GET:
            if "Content-Type" not in local_headers:
                local_headers["Content-Type"] = "application/json"

        payload = json.dumps(data) if data is not None else ""
        request = RESTRequest(
            method=method,
            url=url,
            params=params,
            data=payload,
            headers=local_headers,
            is_auth_required=is_auth_required,
        )

        response = await self.call(request=request, timeout=timeout)
        if 400 <= response.status:
            if not ret_err:
                error_response = await response.text()
                error_text = "N/A" if "<htlm" in error_response else error_response
                raise IOError(
                    f"Error executing request {method.name} {url}. HTTP status is {response.status}. "
                    f"Error: {error_text}"
                )
        return response

    async def call(
        self, request: RESTRequest, timeout: Optional[float] = None
    ) -> RESTResponse:
        request = deepcopy(request)
        request = await self._authenticate(request)
        resp = await self._connection.call(request)
        return resp

    async def _authenticate(self, request: RESTRequest):
        if self._auth is not None and request.is_auth_required:
            request = await self._auth.rest_authenticate(request)
        return request
