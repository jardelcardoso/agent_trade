import os
import textwrap

def create_project():
    # Dicionário contendo todos os caminhos e códigos do projeto
    files = {
        "requirements.txt": r'''
            pandas==2.2.0
            python-binance==1.0.19
            SQLAlchemy==2.0.25
            openai==1.12.0
            python-dotenv==1.0.1
            PyYAML==6.0.1
            ta==0.11.0
        ''',
        ".env": r'''
            BINANCE_API_KEY=sua_chave_binance_aqui
            BINANCE_API_SECRET=seu_secret_binance_aqui
            OPENAI_API_KEY=sua_chave_openai_aqui
        ''',
        "config/settings.yaml": r'''
            execution_mode:
              dry_run: true
              timeframe: "15m"

            risk_management:
              risk_per_trade_percent: 1.0
              max_daily_drawdown: 5.0
              default_stop_loss_pct: 2.0
        ''',
        "config/agent_prompts.py": r'''
            SYSTEM_PROMPT = """Você é um Agente Autónomo de Trading Quantitativo.
            A sua responsabilidade é avaliar as condições técnicas do mercado e decidir a próxima ação.

            REGRAS RÍGIDAS:
            1. A sua resposta DEVE começar obrigatoriamente com uma destas três palavras: COMPRAR, VENDER ou AGUARDAR.
            2. Após a palavra-chave principal, forneça uma justificação lógica em no máximo 2 frases baseada nos dados recebidos.

            EXEMPLOS DE RESPOSTA:
            "COMPRAR. O RSI está sobrevendido e a tendência curta cruzou para alta, indicando um bom ponto de entrada."
            "AGUARDAR. O mercado está lateralizado e o volume é baixo, o risco não compensa."
            "VENDER. O RSI está em zona de sobrecompra extrema e há fraqueza na tendência."
            """
        ''',
        "database.py": r'''
            import os
            from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
            from sqlalchemy.orm import declarative_base, sessionmaker

            os.makedirs("data", exist_ok=True)
            DB_PATH = "sqlite:///data/trading_db.sqlite"
            engine = create_engine(DB_PATH, echo=False)
            Base = declarative_base()
            SessionLocal = sessionmaker(bind=engine)

            class MarketData(Base):
                __tablename__ = "market_data"
                id = Column(Integer, primary_key=True, autoincrement=True)
                symbol = Column(String, index=True)
                timestamp = Column(DateTime, index=True)
                open = Column(Float)
                high = Column(Float)
                low = Column(Float)
                close = Column(Float)
                volume = Column(Float)

            class TradesLog(Base):
                __tablename__ = "trades_log"
                id = Column(Integer, primary_key=True, autoincrement=True)
                timestamp = Column(DateTime)
                symbol = Column(String)
                action = Column(String)
                price = Column(Float)
                quantity = Column(Float)
                is_dry_run = Column(Boolean)
                reason = Column(String)

            def init_db():
                Base.metadata.create_all(engine)
                print("Banco de dados SQLite inicializado com sucesso em data/trading_db.sqlite")

            if __name__ == "__main__":
                init_db()
        ''',
        "src/__init__.py": "",
        "src/agent/__init__.py": "",
        "src/tools/__init__.py": "",
        "src/risk/__init__.py": "",
        "src/brokers/__init__.py": "",
        "src/tools/market_data.py": r'''
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
                    klines = self.client.get_historical_klines(symbol, interval, start_str)
                    
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
        ''',
        "src/tools/tech_analysis.py": r'''
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
        ''',
        "src/brokers/base_broker.py": r'''
            from abc import ABC, abstractmethod

            class BaseBroker(ABC):
                @abstractmethod
                def execute_order(self, symbol: str, action: str, quantity: float, price: float = None):
                    pass
        ''',
        "src/brokers/binance.py": r'''
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
        ''',
        "src/risk/risk_manager.py": r'''
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
        ''',
        "src/agent/orchestrator.py": r'''
            import os
            from openai import OpenAI
            from config.agent_prompts import SYSTEM_PROMPT
            from src.tools.tech_analysis import TechAnalysisTool
            from src.risk.risk_manager import RiskManager
            from src.tools.market_data import MarketDataTool

            class AgentOrchestrator:
                def __init__(self):
                    self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                    self.ta_tool = TechAnalysisTool()
                    self.risk_manager = RiskManager()
                    self.market_tool = MarketDataTool()

                def run_cycle(self, symbol: str):
                    print(f"\n--- Iniciando Ciclo de IA para {symbol} ---")
                    
                    self.market_tool.fetch_and_save_incremental(symbol)
                    tech_summary = self.ta_tool.analyze(symbol)
                    
                    print(f"📊 Leitura da Ferramenta: {tech_summary}")
                    if "Dados insuficientes" in tech_summary:
                        print("Abortando ciclo por falta de dados.")
                        return

                    messages = [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"Mercado atual: {tech_summary}. Qual a sua decisão e porquê?"}
                    ]
                    
                    print("🧠 IA a analisar contexto...")
                    try:
                        response = self.client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=messages,
                            max_tokens=100,
                            temperature=0.2
                        )
                        decisao_ia = response.choices[0].message.content.strip()
                        print(f"🗣️ Resposta da IA: {decisao_ia}")
                        
                    except Exception as e:
                        print(f"Erro ao contactar a OpenAI: {e}")
                        return

                    acao = decisao_ia.split(".")[0].split(" ")[0].upper()
                    
                    if acao in ["COMPRAR", "VENDER"]:
                        df_atual = self.market_tool.get_data_for_analysis(symbol, limit=1)
                        preco = df_atual.iloc[-1]['close']
                        self.risk_manager.evaluate_and_execute(symbol, acao, preco, decisao_ia)
                    else:
                        print("⚖️ Ação descartada ou IA decidiu AGUARDAR.")
        ''',
        "main.py": r'''
            import time
            from dotenv import load_dotenv
            from database import init_db
            from src.agent.orchestrator import AgentOrchestrator

            def main():
                print("Inicializando o Agent Trade...")
                load_dotenv()
                init_db()
                
                agent = AgentOrchestrator()
                symbol = "BTCUSDT"
                
                while True:
                    try:
                        agent.run_cycle(symbol)
                        print("💤 Ciclo concluído. A aguardar o próximo período (15m)...\n")
                        time.sleep(60) 
                        
                    except KeyboardInterrupt:
                        print("\nEncerrando o agente com segurança...")
                        break
                    except Exception as e:
                        print(f"Erro crítico no loop: {e}")
                        time.sleep(60)

            if __name__ == "__main__":
                main()
        '''
    }

    # Motor de criação das pastas e ficheiros
    for file_path, content in files.items():
        dir_name = os.path.dirname(file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(textwrap.dedent(content).strip() + "\n")
            
    print("\n✅ Sucesso! O seu projeto foi estruturado corretamente.")
    print("📌 Próximos passos:")
    print("1. Instale as bibliotecas executando: pip install -r requirements.txt")
    print("2. Preencha o ficheiro recém-criado '.env' com as suas chaves da API")
    print("3. Inicie o robô executando: python main.py")

if __name__ == "__main__":
    create_project()