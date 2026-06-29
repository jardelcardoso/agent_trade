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
