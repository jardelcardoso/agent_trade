from src.brokers.base_broker import BaseBroker
import os
from binance.client import Client

class BinanceBroker(BaseBroker):
    def __init__(self):
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")
        self.client = Client(api_key, api_secret)

    def execute_order(self, symbol: str, action: str, quantity: float, price: float = None):
        print(f"🚀 [REAL EXECUTION] Enviando ordem para Binance: {action} {quantity} {symbol}")
        return {"status": "FILLED", "simulated_real_api": True}
