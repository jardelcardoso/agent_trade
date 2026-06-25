from __future__ import annotations

from pathlib import Path
from typing import Any

from src.agent.decision_policy import DecisionPolicy
from src.agent.memory import AgentMemory
from src.brokers.dry_run_broker import DryRunBroker
from src.risk.risk_manager import RiskManager
from src.tools.market_data import MarketDataService
from src.tools.tech_analysis import TechnicalAnalysisService


class Orchestrator:
    """Orquestra um ciclo simples do agente em modo dry run."""

    def __init__(
        self,
        settings_path: str | Path | None = None,
        db_path: str | Path | None = None,
        broker: object | None = None,
    ) -> None:
        self.db_path = Path(db_path or "data/trading_db.sqlite")
        self.market_data_service = MarketDataService(db_path=self.db_path)
        self.tech_analysis_service = TechnicalAnalysisService(db_path=self.db_path)
        self.risk_manager = RiskManager(settings_path=settings_path, db_path=self.db_path)
        self.memory = AgentMemory(db_path=self.db_path)
        self.decision_policy = DecisionPolicy()
        self.broker = broker or DryRunBroker()

    def run_cycle(self) -> dict[str, Any]:
        candles = [
            {
                "timestamp": "2024-01-01T00:00:00",
                "open": 100.0,
                "high": 101.0,
                "low": 99.0,
                "close": 100.5,
                "volume": 10.0,
            }
        ]
        market_data_inserted = self.market_data_service.sync_market_data("BTCUSDT", candles)
        recent_decisions = self.memory.get_recent_decisions("BTCUSDT", limit=3)
        signal = self.tech_analysis_service.analyze("BTCUSDT", limit=3)
        decision = self.decision_policy.decide(signal["signal"], recent_decisions)
        side = "BUY" if decision == "buy" else "HOLD"
        trade_result = self.risk_manager.validate_trade(
            symbol="BTCUSDT",
            quantity=0.015,
            side=side,
            entry_price=65000.0,
        )
        broker_result = self.broker.place_order("BTCUSDT", side, 0.015, 65000.0)
        self.memory.save_decision("BTCUSDT", decision, trade_result["status"], "now")

        return {
            "status": trade_result["status"],
            "market_data_inserted": market_data_inserted,
            "trade_status": trade_result["status"],
            "signal": signal["signal"],
            "decision": decision,
            "recent_decisions": recent_decisions,
            "broker_result": broker_result,
            "message": trade_result["message"],
        }
