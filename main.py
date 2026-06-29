import time
import yaml
import logging
import os
from dotenv import load_dotenv
from database import init_db
from src.agent.orchestrator import AgentOrchestrator

# Configuração de Logging com codificação UTF-8 forçada para resolver erros no Windows
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/agent.log", encoding='utf-8'), # Força UTF-8 no arquivo
        logging.StreamHandler()
    ]
)

def main():
    load_dotenv()
    init_db()
    
    with open("config/settings.yaml", "r") as f:
        settings = yaml.safe_load(f)
    
    agent = AgentOrchestrator()
    symbols = settings["execution_mode"]["active_symbols"]
    
    logging.info(f"🚀 Agente v2.0 iniciado para: {symbols}")
    
    while True:
        for symbol in symbols:
            try:
                agent.run_cycle(symbol)
            except Exception as e:
                logging.error(f"❌ Erro no ciclo para {symbol}: {e}")
            time.sleep(10)
            
        logging.info("💤 Ciclo completo. Aguardando próximo período...")
        time.sleep(300)

if __name__ == "__main__":
    main()