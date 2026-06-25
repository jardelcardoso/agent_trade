from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class MarketDataService:
    """Gerencia a ingestão incremental de candles em SQLite."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        self.db_path = Path(db_path or "data/trading_db.sqlite")
        self._ensure_db()

    def _ensure_db(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS market_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    open REAL NOT NULL,
                    high REAL NOT NULL,
                    low REAL NOT NULL,
                    close REAL NOT NULL,
                    volume REAL NOT NULL,
                    UNIQUE(symbol, timestamp)
                )
                """
            )

    def sync_market_data(self, symbol: str, candles: list[dict[str, Any]]) -> int:
        if not candles:
            return 0

        with sqlite3.connect(self.db_path) as conn:
            inserted = 0
            for candle in candles:
                cursor = conn.execute(
                    """
                    INSERT OR IGNORE INTO market_data (symbol, timestamp, open, high, low, close, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        symbol,
                        candle["timestamp"],
                        candle["open"],
                        candle["high"],
                        candle["low"],
                        candle["close"],
                        candle["volume"],
                    ),
                )
                if cursor.rowcount == 1:
                    inserted += 1
            conn.commit()

        return inserted

    def get_last_timestamp(self, symbol: str) -> str | None:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT timestamp FROM market_data WHERE symbol = ? ORDER BY timestamp DESC LIMIT 1",
                (symbol,),
            ).fetchone()
        return row[0] if row else None
