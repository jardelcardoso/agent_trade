from __future__ import annotations

from typing import Any


class DecisionPolicy:
    """Aplica regras simples para transformar contexto em uma decisão de trade."""

    def decide(self, signal: str, recent_decisions: list[dict[str, Any]]) -> str:
        if signal == "buy":
            if recent_decisions and recent_decisions[0].get("decision") == "sell":
                return "hold"
            return "buy"

        if signal == "sell":
            if recent_decisions and recent_decisions[0].get("decision") == "buy":
                return "hold"
            return "sell"

        return "hold"
