import yaml
import datetime
from database import SessionLocal, TradesLog
from src.brokers.binance import BinanceBroker

class RiskManager:
    def __init__(self):
        with open("config/settings.yaml", "r") as file:
            self.settings = yaml.safe_load(file)

        self.is_dry_run = self.settings["execution_mode"]["dry_run"]
        self.risk_pct = self.settings["risk_management"]["risk_per_trade_percent"]
        self.db_session = SessionLocal()
        self.broker = BinanceBroker()

    def evaluate_and_execute(self, symbol: str, action: str, current_price: float, reason: str):
        banca_simulada = 1000.00 # USD
        risco_financeiro = banca_simulada * (self.risk_pct / 100)
        quantidade = round(risco_financeiro / current_price, 5)

        if quantidade <= 0:
            print("🛡️ RiskManager bloqueou a operação: Lote calculado muito baixo.")
            return

        if self.is_dry_run:
            print(f"👻 [DRY RUN] Executando ordem fantasma: {action} {quantidade} {symbol} a ${current_price:.2f}")
            self._log_trade(symbol, action, current_price, quantidade, True, reason)
        else:
            self.broker.execute_order(symbol, action, quantidade)
            self._log_trade(symbol, action, current_price, quantidade, False, reason)

    def _log_trade(self, symbol, action, price, quantity, is_dry_run, reason):
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
