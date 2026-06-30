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
from src.tools.sentiment_data import SentimentTool
from src.tools.news_data import NewsDataTool
from src.tools.tech_analysis import TechAnalysisTool
from src.tools.market_data import MarketDataTool

class AgentOrchestrator:
    def __init__(self):
        settings_path = PROJECT_ROOT / "config" / "settings.yaml"
        with settings_path.open("r", encoding="utf-8") as file:
            self.settings = yaml.safe_load(file)
            
        self.providers = self.settings["llm_config"]
        self.current_idx = 0
        self.consecutive_429s = 0
        self._setup_client()
            
        self.ta_tool = TechAnalysisTool()
        self.market_tool = MarketDataTool()
        self.sentiment_tool = SentimentTool()
        self.news_tool = NewsDataTool()

    def _setup_client(self):
        config = self.providers[self.current_idx]
        self.provider = config["provider"]
        self.model_name = config["model_name"]
        
        logging.info(f"Configurando LLM: {self.provider} ({self.model_name})")
        
        if self.provider in {"openai", "openrouter"}:
            api_key = os.getenv("OPENROUTER_API_KEY") if self.provider == "openrouter" else os.getenv("OPENAI_API_KEY")
            client_kwargs = {"api_key": api_key}
            if self.provider == "openrouter":
                client_kwargs["base_url"] = "https://openrouter.ai/api/v1"
                client_kwargs["default_headers"] = {"HTTP-Referer": "http://localhost", "X-Title": "AgentTrade"}
            self.client = OpenAI(**client_kwargs)
        elif self.provider == "gemini":
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel(model_name=self.model_name, system_instruction=SYSTEM_PROMPT)

    def _rotate_provider(self):
        self.current_idx = (self.current_idx + 1) % len(self.providers)
        self.consecutive_429s = 0
        logging.warning(f"🔄 Trocando provedor de IA para: {self.providers[self.current_idx]['provider']}")
        self._setup_client()

    def _call_llm(self, prompt: str):
        try:
            if self.provider in {"openai", "openrouter"}:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
                    temperature=0.2
                )
                self.consecutive_429s = 0
                return response.choices[0].message.content
            
            elif self.provider == "gemini":
                response = self.model.generate_content(prompt)
                self.consecutive_429s = 0
                return response.text.strip()
                    
        except Exception as e:
            if "429" in str(e):
                self.consecutive_429s += 1
                logging.warning(f"⚠️ Erro 429 ({self.consecutive_429s}/3) no {self.provider}")
                if self.consecutive_429s >= 3:
                    self._rotate_provider()
                time.sleep(10)
            else:
                logging.error(f"❌ Erro ao contactar LLM: {e}")
            return None

    def define_market_regime(self, symbol: str) -> str:
        logging.info(f"🧠 Convocando Reunião Macro para {symbol}...")
        sentimento = self.sentiment_tool.get_fear_and_greed()
        noticias = self.news_tool.get_crypto_news(symbol)
        
        prompt = (f"Ativo: {symbol}. Sentimento: {sentimento}. Manchetes: {noticias}. "
                  "Qual o regime atual? (BULLISH, BEARISH ou NEUTRAL). Apenas uma palavra.")
        
        resposta = self._call_llm(prompt)
        regime = "NEUTRAL"
        if resposta:
            regime = "".join([c for c in resposta if c.isalpha()]).upper()
            if regime not in ["BULLISH", "BEARISH", "NEUTRAL"]: regime = "NEUTRAL"
            
        file_path = f"data/{symbol}_regime.txt"
        os.makedirs("data", exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f: f.write(regime)
        
        logging.info(f"👔 Veredito para {symbol}: {regime}")
        return regime

    def run_cycle(self, symbol: str):
        # Método mantido para compatibilidade se necessário...
        pass