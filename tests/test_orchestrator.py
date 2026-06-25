import sqlite3
from pathlib import Path

from src.agent.orchestrator import Orchestrator


def test_orchestrator_executes_dry_run_cycle(tmp_path: Path) -> None:
    db_path = tmp_path / "trading_db.sqlite"
    settings_path = tmp_path / "settings.yaml"
    settings_path.write_text(
        "execution_mode:\n  dry_run: true\n"
        "risk_management:\n  risk_per_trade_percent: 1.0\n",
        encoding="utf-8",
    )

    orchestrator = Orchestrator(settings_path=settings_path, db_path=db_path)
    result = orchestrator.run_cycle()

    assert "dry_run" in result["status"].lower()
    assert result["market_data_inserted"] == 1
    assert result["trade_status"] == "dry_run"

    with sqlite3.connect(db_path) as conn:
        market_rows = conn.execute("SELECT symbol FROM market_data").fetchall()
        trade_rows = conn.execute("SELECT status FROM trades_log").fetchall()

    assert market_rows == [("BTCUSDT",)]
    assert trade_rows == [("dry_run",)]
