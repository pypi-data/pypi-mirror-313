from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .data_types import RESTRequest, WSRequest


class BaseAuth(ABC):
    """
    Abstract base class for WebSocket authentication.

    This class defines the interface for WebSocket authentication that
    must be implemented by any subclass. It uses the `abc` module to
    enforce the implementation of the `ws_authenticate` method.
    """

    @abstractmethod
    async def ws_authenticate(self, request: "WSRequest") -> "WSRequest":
        """
        Authenticate a WebSocket request.

        This method should be implemented by subclasses to provide
        specific authentication logic for WebSocket requests.

        Args:
            request (WSRequest): The WebSocket request to authenticate.

        Returns:
            WSRequest: The authenticated WebSocket request.
        """
        pass

    @abstractmethod
    async def rest_authenticate(self, request: "RESTRequest") -> "RESTRequest":
        pass
