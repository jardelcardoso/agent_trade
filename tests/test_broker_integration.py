from pathlib import Path

from src.agent.orchestrator import Orchestrator
from src.brokers.dry_run_broker import DryRunBroker


def test_orchestrator_uses_broker_when_provided(tmp_path: Path) -> None:
    settings_path = tmp_path / "settings.yaml"
    settings_path.write_text(
        "execution_mode:\n  dry_run: true\n"
        "risk_management:\n  risk_per_trade_percent: 1.0\n",
        encoding="utf-8",
    )

    orchestrator = Orchestrator(settings_path=settings_path, db_path=tmp_path / "trading_db.sqlite", broker=DryRunBroker())
    result = orchestrator.run_cycle()

    assert result["broker_result"]["status"] == "dry_run"
