from dataclasses import dataclass


@dataclass
class ConnectorURL:
    PUBLIC_SPOT: str
    PUBLIC_LINEAR: str
    PUBLIC_INVERSE: str
    TRADE: str
    BASE: str
    PRIVATE: str
