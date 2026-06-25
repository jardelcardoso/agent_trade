from __future__ import annotations

from src.brokers.base_broker import Broker


class DryRunBroker:
    """Implementação fake para o modo dry run."""

    def place_order(self, symbol: str, side: str, quantity: float, price: float | None = None) -> dict[str, object]:
        return {
            "status": "dry_run",
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
        }
