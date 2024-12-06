from dataclasses import dataclass

from .enums import EConnectorStatus, EWebSocketType


@dataclass
class ConnectorStatus:
    msg: str
    status: EConnectorStatus
    websocket_type: EWebSocketType
