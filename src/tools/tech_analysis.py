from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class TechnicalAnalysisService:
    """Calcula sinais simples a partir de candles salvos em SQLite."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        self.db_path = Path(db_path or "data/trading_db.sqlite")

    def analyze(self, symbol: str, limit: int = 3) -> dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT timestamp, close
                FROM market_data
                WHERE symbol = ?
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (symbol, limit),
            ).fetchall()

        if len(rows) < 2:
            return {"signal": "hold", "reason": "not_enough_data"}

        closes = [row[1] for row in rows]
        latest = closes[0]
        previous = closes[-1]
        change = latest - previous
        average = sum(closes) / len(closes)

        if latest > average and change > 0:
            signal = "buy"
        elif latest < average and change < 0:
            signal = "sell"
        else:
            signal = "hold"

        return {
            "signal": signal,
            "reason": "simple_momentum",
            "latest_close": latest,
            "previous_close": previous,
            "average_close": average,
        }
