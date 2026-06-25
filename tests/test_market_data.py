import sqlite3
from pathlib import Path

from src.tools.market_data import MarketDataService


def test_sync_market_data_persists_new_candles(tmp_path: Path) -> None:
    db_path = tmp_path / "trading_db.sqlite"
    service = MarketDataService(db_path=db_path)

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

    inserted = service.sync_market_data("BTCUSDT", candles)
    assert inserted == 1

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute("SELECT symbol, timestamp FROM market_data").fetchall()

    assert rows == [("BTCUSDT", "2024-01-01T00:00:00")]
    assert service.get_last_timestamp("BTCUSDT") == "2024-01-01T00:00:00"
