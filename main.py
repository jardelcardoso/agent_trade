import time
import yaml
import logging
import os
from dotenv import load_dotenv
from database import init_db
from src.agent.orchestrator import AgentOrchestrator
from src.agent.tech_trader import TechTrader

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("logs/agent.log", encoding='utf-8'), logging.StreamHandler()]
)

def main():
    load_dotenv()
    init_db()
    
    with open("config/settings.yaml", "r") as f:
        settings = yaml.safe_load(f)
    
    estrategista_ia = AgentOrchestrator()
    robo_executor = TechTrader()
    
    symbols = settings["execution_mode"]["active_symbols"]
    logging.info(f"🚀 Iniciando Sistema Institucional V3.0 para: {symbols}")
    
    ciclos_executados = 0
    
    while True:
        try:
            # A cada 12 ciclos (ex: 1 hora se o loop tiver 5 min), a IA lê as notícias e define o Regime.
            if ciclos_executados % 12 == 0:
                for symbol in symbols:
                    estrategista_ia.define_market_regime(symbol)
                    time.sleep(5) # Pausa leve entre chamadas de IA para evitar Rate Limits
            
            # O Robô Matemático Rápido roda sempre
            for symbol in symbols:
                robo_executor.execute_fast_cycle(symbol)
                time.sleep(2) # Pausa leve entre moedas
                
            logging.info("💤 Varredura técnica concluída. Aguardando 5 minutos...")
            ciclos_executados += 1
            time.sleep(300) # Roda a matemática a cada 5 minutos
            
        except KeyboardInterrupt:
            logging.info("\nEncerrando o sistema com segurança...")
            break
        except Exception as e:
            logging.error(f"Erro crítico no loop principal: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()