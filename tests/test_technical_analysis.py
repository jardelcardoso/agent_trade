from pathlib import Path

import sqlite3

from src.tools.market_data import MarketDataService
from src.tools.tech_analysis import TechnicalAnalysisService


def test_technical_analysis_returns_buy_signal_for_uptrend(tmp_path: Path) -> None:
    db_path = tmp_path / "trading_db.sqlite"
    market_service = MarketDataService(db_path=db_path)
    analysis_service = TechnicalAnalysisService(db_path=db_path)

    candles = [
        {
            "timestamp": "2024-01-01T00:00:00",
            "open": 100.0,
            "high": 101.0,
            "low": 99.0,
            "close": 102.0,
            "volume": 10.0,
        },
        {
            "timestamp": "2024-01-01T01:00:00",
            "open": 102.0,
            "high": 103.0,
            "low": 101.0,
            "close": 104.0,
            "volume": 10.0,
        },
        {
            "timestamp": "2024-01-01T02:00:00",
            "open": 104.0,
            "high": 105.0,
            "low": 103.0,
            "close": 106.0,
            "volume": 10.0,
        },
    ]

    market_service.sync_market_data("BTCUSDT", candles)
    result = analysis_service.analyze("BTCUSDT", limit=3)

    assert result["signal"] == "buy"
    assert result["latest_close"] == 106.0
