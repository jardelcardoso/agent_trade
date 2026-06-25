from pathlib import Path

from src.agent.memory import AgentMemory
from src.agent.orchestrator import Orchestrator


def test_orchestrator_includes_recent_memory_context(tmp_path: Path) -> None:
    db_path = tmp_path / "trading_db.sqlite"
    settings_path = tmp_path / "settings.yaml"
    settings_path.write_text(
        "execution_mode:\n  dry_run: true\n"
        "risk_management:\n  risk_per_trade_percent: 1.0\n",
        encoding="utf-8",
    )

    memory = AgentMemory(db_path=db_path)
    memory.save_decision("BTCUSDT", "buy", "dry_run", "2024-01-01T00:00:00")

    orchestrator = Orchestrator(settings_path=settings_path, db_path=db_path)
    result = orchestrator.run_cycle()

    assert "recent_decisions" in result
    assert result["recent_decisions"][0]["decision"] == "buy"
