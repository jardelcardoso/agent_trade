from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class AgentMemory:
    """Armazena e recupera decisões do agente em SQLite."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        self.db_path = Path(db_path or "data/trading_db.sqlite")
        self._ensure_db()

    def _ensure_db(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS agent_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    def save_decision(self, symbol: str, decision: str, status: str, created_at: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO agent_memory (symbol, decision, status, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (symbol, decision, status, created_at),
            )
            conn.commit()
        return int(cursor.lastrowid)

    def get_recent_decisions(self, symbol: str, limit: int = 5) -> list[dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT symbol, decision, status, created_at
                FROM agent_memory
                WHERE symbol = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (symbol, limit),
            ).fetchall()

        return [
            {"symbol": row[0], "decision": row[1], "status": row[2], "created_at": row[3]}
            for row in rows
        ]
