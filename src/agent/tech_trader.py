import logging
import os
from src.tools.tech_analysis import TechAnalysisTool
from src.tools.market_data import MarketDataTool
from src.risk.risk_manager import RiskManager

class TechTrader:
    """Versão 3.0: Algoritmo puro de Python. O Executor consciente da posição."""
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
        # 1. Recupera o Contexto
        regime = self._get_current_regime(symbol)
        posicao = self.risk_manager.get_position(symbol) # O SEU ESTOQUE ATUAL
        
        logging.info(f"⚡ Varredura Técnica [{symbol}] | Regime: {regime} | Posição Atual: {posicao}")
        
        self.market_tool.fetch_and_save_incremental(symbol)
        df = self.market_tool.get_data_for_analysis(symbol, limit=100)
        
        if df.empty or len(df) < 50:
            return

        import ta
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
        df['sma_20'] = ta.trend.SMAIndicator(df['close'], window=20).sma_indicator()
        
        last_row = df.iloc[-1]
        preco = last_row['close']
        rsi = last_row['rsi']
        sma20 = last_row['sma_20']
        
        # Lógica de decisão consciente da posição
        acao = "MANTER"
        motivo = "Condições não atendidas para mudança de posição."

        # === REGRAS DE EXECUÇÃO ===
        if regime == "BULLISH":
            # Se não tem posição e RSI está baixo, compra
            if posicao <= 0 and rsi < 35 and preco > sma20:
                acao = "COMPRAR"
                motivo = "Regime BULLISH: Entrada técnica em RSI baixo."
            # Se já tem posição e RSI está muito alto, vende
            elif posicao > 0 and rsi > 75:
                acao = "VENDER"
                motivo = "Regime BULLISH: Realização de lucro (RSI esticado)."

        elif regime == "BEARISH":
            # Se tem posição aberta no Bear Market, vende imediatamente para estancar sangria
            if posicao > 0:
                acao = "VENDER"
                motivo = "Regime BEARISH: Liquidação de proteção (Stop Loss/Redução)."
            # Se não tem posição, fica parado (não faz nada)

        elif regime == "NEUTRAL":
            # Compra apenas em pânico absoluto
            if posicao <= 0 and rsi < 25:
                acao = "COMPRAR"
                motivo = "Regime NEUTRAL: Compra de pânico (oversold)."
            # Vende se estiver esticado
            elif posicao > 0 and rsi > 70:
                acao = "VENDER"
                motivo = "Regime NEUTRAL: Saída técnica."

        # Execução final
        if acao in ["COMPRAR", "VENDER"]:
            self.risk_manager.evaluate_and_execute(symbol, acao, preco, motivo)
        else:
            logging.info(f"🛡️ {acao}: Sem necessidade de mudar posição atual de {posicao} {symbol}.")
