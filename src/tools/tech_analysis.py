import pandas as pd
import ta
from src.tools.market_data import MarketDataTool

class TechAnalysisTool:
    def __init__(self):
        self.market_tool = MarketDataTool()

    def analyze(self, symbol: str) -> str:
        df = self.market_tool.get_data_for_analysis(symbol, limit=100)

        if df.empty or len(df) < 50:
            return "Dados insuficientes para análise técnica."

        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
        df['sma_20'] = ta.trend.SMAIndicator(df['close'], window=20).sma_indicator()
        df['sma_50'] = ta.trend.SMAIndicator(df['close'], window=50).sma_indicator()

        last_row = df.iloc[-1]
        preco_atual = last_row['close']
        rsi_atual = last_row['rsi']
        sma20 = last_row['sma_20']
        sma50 = last_row['sma_50']

        tendencia = "ALTA" if sma20 > sma50 else "BAIXA"

        estado_rsi = "Neutro"
        if rsi_atual < 30:
            estado_rsi = "Sobrevendido (Possível reversão para alta)"
        elif rsi_atual > 70:
            estado_rsi = "Sobrecomprado (Possível reversão para baixa)"

        resumo = (
            f"Preço Atual: {preco_atual:.2f}. "
            f"Tendência baseada em médias: {tendencia}. "
            f"RSI (14): {rsi_atual:.2f} [{estado_rsi}]. "
        )
        return resumo
