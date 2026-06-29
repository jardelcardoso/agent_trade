import yaml
import datetime
import logging
from sqlalchemy.sql import func
from database import SessionLocal, TradesLog
from src.brokers.binance import BinanceBroker

class RiskManager:
    def __init__(self):
        # Carrega configurações
        with open("config/settings.yaml", "r") as file:
            self.settings = yaml.safe_load(file)
            
        self.is_dry_run = self.settings["execution_mode"]["dry_run"]
        self.risk_pct = self.settings["risk_management"]["risk_per_trade_percent"]
        self.db_session = SessionLocal()
        self.broker = BinanceBroker()

    def get_position(self, symbol: str) -> float:
        """Calcula a posição atual do ativo somando compras e subtraindo vendas."""
        buys = self.db_session.query(func.sum(TradesLog.quantity)).filter(
            TradesLog.symbol == symbol, 
            TradesLog.action == "COMPRAR",
            TradesLog.is_dry_run == self.is_dry_run
        ).scalar() or 0.0
        
        sells = self.db_session.query(func.sum(TradesLog.quantity)).filter(
            TradesLog.symbol == symbol, 
            TradesLog.action == "VENDER",
            TradesLog.is_dry_run == self.is_dry_run
        ).scalar() or 0.0
        
        # Arredonda para evitar erros de ponto flutuante (ex: 0.00000001)
        return round(buys - sells, 6)

    def evaluate_and_execute(self, symbol: str, action: str, current_price: float, reason: str):
        """Valida o risco, avalia a posição e interceta se for Dry Run."""
        posicao_atual = self.get_position(symbol)
        
        if action == "VENDER":
            if posicao_atual <= 0:
                logging.warning(f"🛡️ RiskManager bloqueou a operação: Tentativa de VENDER {symbol} sem ter posição aberta.")
                return
            # Se for VENDER, liquidamos toda a posição atual
            quantidade = posicao_atual
            logging.info(f"📉 Preparando para liquidar posição total de {quantidade} {symbol}.")
            
        elif action == "COMPRAR":
            # Simulação de cálculo de lote (Na prática, leria o saldo real da corretora)
            banca_simulada = 1000.00 # USD
            risco_financeiro = banca_simulada * (self.risk_pct / 100)
            
            # Calcula tamanho da posição simplificado
            quantidade = round(risco_financeiro / current_price, 5)
        else:
            return # Se chegar MANTER ou AGUARDAR, simplesmente ignora.

        if quantidade <= 0:
            logging.warning(f"🛡️ RiskManager bloqueou a operação: Lote calculado muito baixo.")
            return

        if self.is_dry_run:
            print(f"👻 [DRY RUN] Executando ordem fantasma: {action} {quantidade} {symbol} a ${current_price:.2f}")
            self._log_trade(symbol, action, current_price, quantidade, True, reason)
        else:
            # Envia ordem real
            self.broker.execute_order(symbol, action, quantidade)
            self._log_trade(symbol, action, current_price, quantidade, False, reason)

    def _log_trade(self, symbol, action, price, quantity, is_dry_run, reason):
        """Guarda o histórico no SQLite."""
        trade = TradesLog(
            timestamp=datetime.datetime.utcnow(),
            symbol=symbol,
            action=action,
            price=price,
            quantity=quantity,
            is_dry_run=is_dry_run,
            reason=reason
        )
        self.db_session.add(trade)
        self.db_session.commit()