import logging

import pandas as pd
from binance.client import Client
from sqlalchemy.sql import func
from database import SessionLocal, MarketData
import os

class MarketDataTool:
    def __init__(self):
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")
        self.client = Client(api_key, api_secret)
        self.db_session = SessionLocal()

    def get_latest_timestamp(self, symbol: str):
        return self.db_session.query(func.max(MarketData.timestamp)).filter(MarketData.symbol == symbol).scalar()

    def fetch_and_save_incremental(self, symbol: str, interval: str = "15m"):
        last_date = self.get_latest_timestamp(symbol)
        start_str = last_date.strftime("%d %b %Y %H:%M:%S") if last_date else "5 days ago UTC"

        print(f"[{symbol}] Sincronizando preços a partir de {start_str}...")
        try:
            klines = self.client.get_historical_klines(symbol, interval, start_str)
        except Exception as e:
            logging.error(f"Erro de conexão com Binance ({symbol}): {e}")
            return False # Apenas retorna False e espera o próximo ciclo

        if not klines:
            return False

        new_records = []
        for k in klines:
            ts = pd.to_datetime(k[0], unit='ms')
            if last_date and ts <= last_date:
                continue

            record = MarketData(
                symbol=symbol,
                timestamp=ts,
                open=float(k[1]),
                high=float(k[2]),
                low=float(k[3]),
                close=float(k[4]),
                volume=float(k[5])
            )
            new_records.append(record)

        if new_records:
            self.db_session.bulk_save_objects(new_records)
            self.db_session.commit()
            print(f"[{symbol}] +{len(new_records)} novas velas inseridas no banco.")
            return True
        return False

    def get_data_for_analysis(self, symbol: str, limit: int = 100) -> pd.DataFrame:
        query = self.db_session.query(MarketData).filter(MarketData.symbol == symbol).order_by(MarketData.timestamp.desc()).limit(limit)
        df = pd.read_sql(query.statement, self.db_session.bind)
        if not df.empty:
            df = df.sort_values('timestamp').reset_index(drop=True)
        return df
