import sqlite3
from pathlib import Path

import yaml

from src.risk.risk_manager import RiskManager


def test_dry_run_trade_is_logged_to_sqlite(tmp_path: Path) -> None:
    settings_path = tmp_path / "settings.yaml"
    settings_path.write_text(
        "execution_mode:\n  dry_run: true\n"
        "risk_management:\n  risk_per_trade_percent: 1.0\n",
        encoding="utf-8",
    )
    db_path = tmp_path / "trading_db.sqlite"

    risk_manager = RiskManager(settings_path=settings_path, db_path=db_path)
    result = risk_manager.validate_trade(
        symbol="BTCUSDT",
        quantity=0.015,
        side="BUY",
        entry_price=65000.0,
    )

    assert result["status"] == "dry_run"
    assert "[DRY RUN]" in result["message"]

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute("SELECT symbol, status FROM trades_log").fetchall()

    assert rows == [("BTCUSDT", "dry_run")]
