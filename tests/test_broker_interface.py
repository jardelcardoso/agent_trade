from src.brokers.dry_run_broker import DryRunBroker


def test_dry_run_broker_returns_simulated_order() -> None:
    broker = DryRunBroker()
    result = broker.place_order("BTCUSDT", "BUY", 0.015, 65000.0)

    assert result["status"] == "dry_run"
    assert result["symbol"] == "BTCUSDT"
    assert result["quantity"] == 0.015
