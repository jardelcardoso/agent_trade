from __future__ import annotations

from typing import Protocol


class Broker(Protocol):
    """Contrato simples para envio de ordens."""

    def place_order(self, symbol: str, side: str, quantity: float, price: float | None = None) -> dict[str, object]:
        ...
