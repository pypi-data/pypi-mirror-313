from dataclasses import dataclass, field
from typing import Dict


@dataclass
class CoinBalance:
    total: float = 0.0
    available: float = 0.0
    realised_pnl: float = 0.0
    unrealised_pnl: float = 0.0


@dataclass
class Wallet:
    wallet: Dict[str, CoinBalance] = field(default_factory=dict)
    timestamp: int = 0
