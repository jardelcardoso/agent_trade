from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import yaml


class RiskManager:
    """Valida operações e registra ordens simuladas quando o modo dry run está ativo."""

    def __init__(self, settings_path: str | Path | None = None, db_path: str | Path | None = None) -> None:
        self.settings_path = Path(settings_path or "config/settings.yaml")
        self.db_path = Path(db_path or "data/trading_db.sqlite")
        self._settings = self._load_settings()
        self._ensure_db()

    def _load_settings(self) -> dict[str, Any]:
        with self.settings_path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle) or {}

    def _ensure_db(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS trades_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    quantity REAL NOT NULL,
                    side TEXT NOT NULL,
                    entry_price REAL NOT NULL,
                    status TEXT NOT NULL,
                    message TEXT NOT NULL
                )
                """
            )

    def validate_trade(self, symbol: str, quantity: float, side: str, entry_price: float) -> dict[str, Any]:
        execution_mode = self._settings.get("execution_mode", {})
        if execution_mode.get("dry_run", True):
            message = f"[DRY RUN] {side} {quantity} {symbol} @ {entry_price}"
            self._log_trade(symbol, quantity, side, entry_price, "dry_run", message)
            return {"status": "dry_run", "message": message}

        return {"status": "live", "message": "Order forwarded to broker adapter"}

    def _log_trade(
        self,
        symbol: str,
        quantity: float,
        side: str,
        entry_price: float,
        status: str,
        message: str,
    ) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO trades_log (symbol, quantity, side, entry_price, status, message)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (symbol, quantity, side, entry_price, status, message),
            )
