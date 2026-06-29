import os
import sys
import time
import logging
from pathlib import Path

from openai import OpenAI
import yaml
import google.generativeai as genai

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.agent_prompts import SYSTEM_PROMPT
from src.tools.tech_analysis import TechAnalysisTool
from src.risk.risk_manager import RiskManager
from src.tools.market_data import MarketDataTool

class AgentOrchestrator:
    def __init__(self):
        # Carrega configurações
        settings_path = PROJECT_ROOT / "config" / "settings.yaml"
        with settings_path.open("r", encoding="utf-8") as file:
            self.settings = yaml.safe_load(file)
            
        self.provider = self.settings["llm_config"]["provider"]  # 'openai', 'openrouter' ou 'gemini'
        self.model_name = self.settings["llm_config"]["model_name"]
        
        if self.provider in {"openai", "openrouter"}:
            api_key = (
                os.getenv("OPENROUTER_API_KEY")
                if self.provider == "openrouter"
                else os.getenv("OPENAI_API_KEY")
            )
            if not api_key:
                raise ValueError(
                    "OPENROUTER_API_KEY não configurada"
                    if self.provider == "openrouter"
                    else "OPENAI_API_KEY não configurada"
                )

            client_kwargs = {"api_key": api_key}
            if self.provider == "openrouter":
                client_kwargs["base_url"] = "https://openrouter.ai/api/v1"
                client_kwargs["default_headers"] = {
                    "HTTP-Referer": os.getenv("OPENROUTER_HTTP_REFERER", "http://localhost"),
                    "X-Title": os.getenv("OPENROUTER_APP_NAME", "AgentTrade"),
                }

            self.client = OpenAI(**client_kwargs)
        elif self.provider == "gemini":
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=SYSTEM_PROMPT
            )
            
        self.ta_tool = TechAnalysisTool()
        self.risk_manager = RiskManager()
        self.market_tool = MarketDataTool()

    def _call_llm(self, prompt: str, retries=3):
        for i in range(retries):
            try:
                if self.provider in {"openai", "openrouter"}:
                    response = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
                        temperature=0.2
                    )
                    return response.choices[0].message.content
                
                elif self.provider == "gemini":
                    response = self.model.generate_content(prompt)
                    return response.text.strip()
                    
            except Exception as e:
                # Tratamento robusto de cota excedida (429) usando loop em vez de recursão
                if "429" in str(e) and i < retries - 1:
                    wait_time = 60 * (i + 1)
                    logging.warning(f"⚠️ Limite de cota atingido (429). Retentativa {i+1} em {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logging.error(f"❌ Erro crítico ao contactar o LLM ({self.provider}): {e}")
                    return "AGUARDAR. Falha no processamento."
        return "AGUARDAR. Limite de tentativas excedido."

    def run_cycle(self, symbol: str):
        logging.info(f"--- [v2.0] Ciclo Iniciado ({self.provider}): {symbol} ---")
        
        self.market_tool.fetch_and_save_incremental(symbol)
        tech_summary = self.ta_tool.analyze(symbol)
        
        if "Dados insuficientes" in tech_summary: 
            logging.warning("Abortando ciclo por falta de dados.")
            return

        # Busca a posição atual no banco de dados
        posicao_atual = self.risk_manager.get_position(symbol)
        status_posicao = f"Você está COMPRADO em {posicao_atual} unidades." if posicao_atual > 0 else "ZERO (Você NÃO possui posições abertas)."

        # Injeta o contexto da carteira no prompt
        prompt_usuario = f"Ativo: {symbol}. Posição Atual na Carteira: {status_posicao}\nDados Técnicos: {tech_summary}. Atue como um especialista em trading. Qual a sua decisão (COMPRAR, VENDER, MANTER ou AGUARDAR) e o fundamento técnico?"
        
        logging.info(f"📝 Prompt enviado à IA: {prompt_usuario}")
        
        decisao_ia = self._call_llm(prompt_usuario)
        logging.info(f"🗣️ Resposta da IA: {decisao_ia}")

        # Extração da ação (COMPRAR/VENDER/AGUARDAR/MANTER)
        acao = decisao_ia.split(".")[0].split(" ")[0].upper()
        
        if acao in ["COMPRAR", "VENDER"]:
            df_atual = self.market_tool.get_data_for_analysis(symbol, limit=1)
            preco = df_atual.iloc[-1]['close']
            self.risk_manager.evaluate_and_execute(symbol, acao, preco, decisao_ia)
        elif acao == "MANTER":
            logging.info(f"🛡️ IA decidiu MANTER a posição atual de {symbol}.")
        else:
            logging.info(f"⚖️ IA decidiu AGUARDAR (Ficar de fora do mercado).")