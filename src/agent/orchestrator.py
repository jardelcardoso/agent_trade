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

class AgentOrchestrator:
    """Versão 3.0: A IA agora é o Estrategista Macro, não o operador de botões."""
    def __init__(self):
        settings_path = PROJECT_ROOT / "config" / "settings.yaml"
        with settings_path.open("r", encoding="utf-8") as file:
            self.settings = yaml.safe_load(file)
            
        self.provider = self.settings["llm_config"]["provider"]
        self.model_name = self.settings["llm_config"]["model_name"]
        
        # Configuração do Provedor (OpenAI, OpenRouter, Gemini)
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
            
        self.sentiment_tool = SentimentTool()

    def _call_llm(self, prompt: str, retries=3):
        for i in range(retries):
            try:
                if self.provider in {"openai", "openrouter"}:
                    res = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
                        temperature=0.2
                    )
                    return res.choices[0].message.content
                elif self.provider == "gemini":
                    return self.model.generate_content(prompt).text.strip()
            except Exception as e:
                if "429" in str(e) and i < retries - 1:
                    time.sleep(60 * (i + 1))
                else:
                    return "NEUTRAL. Erro de API."
        return "NEUTRAL. Fallback de segurança."

    def define_market_regime(self, symbol: str) -> str:
        """Consulta o sentimento, pede a análise da IA e salva o regime atual."""
        logging.info(f"🧠 Convocando Reunião do Comitê de IA (Análise Macro) para {symbol}...")
        
        sentimento = self.sentiment_tool.get_fear_and_greed()
        prompt = f"Ativo em análise: {symbol}. Dados de mercado hoje: {sentimento}. Qual o regime de mercado atual para este ativo?"
        
        resposta_ia = self._call_llm(prompt)
        logging.info(f"👔 Veredito do Estrategista para {symbol}: {resposta_ia}")
        
        # Extrai a palavra-chave e salva em um arquivo local para o robô ler
        regime = resposta_ia.split(".")[0].split(" ")[0].upper()
        if regime not in ["BULLISH", "BEARISH", "NEUTRAL"]:
            regime = "NEUTRAL" # Segurança
            
        # Salva o regime na memória (arquivo simples especifico por ativo)
        with open(f"data/{symbol}_regime.txt", "w", encoding="utf-8") as f:
            f.write(regime)
            
        return regime