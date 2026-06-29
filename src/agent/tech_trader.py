import logging
import os
from src.tools.tech_analysis import TechAnalysisTool
from src.tools.market_data import MarketDataTool
from src.risk.risk_manager import RiskManager

class TechTrader:
    """Versão 3.0: Algoritmo puro de Python. Executa rápido e sem atrasos (Zero IA aqui)."""
    def __init__(self):
        self.ta_tool = TechAnalysisTool()
        self.market_tool = MarketDataTool()
        self.risk_manager = RiskManager()
    def _get_current_regime(self, symbol: str):
        """Lê a ordem ditada pelo Estrategista (IA)."""
        file_path = f"data/{symbol}_regime.txt"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        return "NEUTRAL"

    def execute_fast_cycle(self, symbol: str):
        regime = self._get_current_regime(symbol)
        logging.info(f"⚡ Iniciando Varredura Técnica [{symbol}] | Regime Permitido: {regime}")
        
        self.market_tool.fetch_and_save_incremental(symbol)
        df = self.market_tool.get_data_for_analysis(symbol, limit=100)
        
        if df.empty or len(df) < 50:
            logging.warning("Sem dados suficientes.")
            return

        # Calcula indicadores matemáticos (rápido, exato)
        import ta
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
        df['sma_20'] = ta.trend.SMAIndicator(df['close'], window=20).sma_indicator()
        
        last_row = df.iloc[-1]
        preco = last_row['close']
        rsi = last_row['rsi']
        sma20 = last_row['sma_20']
        
        posicao = self.risk_manager.get_position(symbol)
        acao = "MANTER"
        motivo = ""

        # ==========================================
        # LÓGICA INSTITUCIONAL (Regime + Matemática)
        # ==========================================
        if regime == "BULLISH":
            if rsi < 35 and preco > sma20:
                acao = "COMPRAR"
                motivo = "Regime BULLISH + RSI Sobrevendido em Tendência de Alta."
            elif rsi > 75 and posicao > 0:
                acao = "VENDER"
                motivo = "Realização de lucros em zona de super-euforia."

        elif regime == "BEARISH":
            if posicao > 0:
                acao = "VENDER"
                motivo = "Regime BEARISH decretado. Cortando risco (Stop)."
            # Não fazemos compras (Long) em Bear Market no nosso MVP.

        elif regime == "NEUTRAL":
            if rsi < 25: # Exige um desconto muito maior para comprar
                acao = "COMPRAR"
                motivo = "Pânico extremo identificado durante regime Neutro."
            elif rsi > 70 and posicao > 0:
                acao = "VENDER"
                motivo = "Regime Neutro + RSI esticado. Saindo da operação."

        # Execução final
        if acao in ["COMPRAR", "VENDER"]:
            self.risk_manager.evaluate_and_execute(symbol, acao, preco, motivo)
        else:
            logging.info(f"🛡️ Nenhuma oportunidade exata matemática encontrada para {symbol} agora.")