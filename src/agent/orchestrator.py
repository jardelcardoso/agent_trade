import os
import sys
import time
import logging
from pathlib import Path

from openai import OpenAI
import yaml
import google.generativeai as genai

# Resolve os caminhos para permitir execução a partir de qualquer diretório
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.agent_prompts import SYSTEM_PROMPT
from src.tools.sentiment_data import SentimentTool
from src.tools.news_data import NewsDataTool

class AgentOrchestrator:
    """
    V3.0 - O Estrategista Chefe.
    Responsável apenas por ler o contexto macro (Notícias + Sentimento)
    e ditar o "Regime" de mercado (BULLISH, BEARISH, NEUTRAL) para o robô executor.
    """
    def __init__(self):
        # Carrega configurações
        settings_path = PROJECT_ROOT / "config" / "settings.yaml"
        with settings_path.open("r", encoding="utf-8") as file:
            self.settings = yaml.safe_load(file)
            
        self.provider = self.settings["llm_config"]["provider"]  # 'openai', 'openrouter' ou 'gemini'
        self.model_name = self.settings["llm_config"]["model_name"]
        
        # Inicialização do Cliente LLM baseado no provedor escolhido
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
            
        # Instancia as ferramentas macro
        self.sentiment_tool = SentimentTool()
        self.news_tool = NewsDataTool()

    def _call_llm(self, prompt: str, retries=3):
        """Chama a IA com tratamento robusto de Rate Limits (429)."""
        for i in range(retries):
            try:
                if self.provider in {"openai", "openrouter"}:
                    response = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
                        temperature=0.2
                    )
                    if response.choices[0].message.content:
                        return response.choices[0].message.content
                    return "AGUARDAR. Resposta vazia da IA."
                
                elif self.provider == "gemini":
                    response = self.model.generate_content(prompt)
                    return response.text.strip()
                    
            except Exception as e:
                # Fallback em caso de falha de conexão ou Rate Limit excessivo
                if "429" in str(e) and i < retries - 1:
                    wait_time = 30 * (i + 1)
                    logging.warning(f"⚠️ Limite de cota atingido (429). Retentativa {i+1} em {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logging.error(f"❌ Erro crítico ao contactar o LLM ({self.provider}): {e}")
                    return "NEUTRAL" 
        return "NEUTRAL"

    def define_market_regime(self, symbol: str) -> str:
        """
        Consulta o sentimento global e as notícias específicas da moeda,
        pede a análise da IA e salva o regime no disco.
        """
        logging.info(f"🧠 Convocando Reunião Macro para {symbol} (Sentimento + Notícias)...")
        
        # 1. Coleta dados brutos das ferramentas (O "Mundo Real")
        sentimento = self.sentiment_tool.get_fear_and_greed()
        noticias = self.news_tool.get_crypto_news(symbol)
        
        # 2. Constrói o Prompt contextualizado para o ativo
        prompt = (
            f"Ativo em análise: {symbol}.\n\n"
            f"1. Sentimento Global (Fear & Greed): {sentimento}\n"
            f"2. Últimas Manchetes sobre o ativo:\n{noticias}\n\n"
            "Atue como um Estrategista Chefe. Avaliando o medo/ganância e o tom das notícias recentes, "
            "qual o regime de mercado atual para este ativo? Responda APENAS com uma destas palavras: BULLISH, BEARISH ou NEUTRAL."
        )
        
        logging.info(f"📰 Lendo manchetes para a IA...\n{noticias}")
        
        # 3. Deliberação da IA
        logging.info(f"🤖 Enviando prompt para IA ({self.provider}):\n{prompt}")
        resposta_ia = self._call_llm(prompt)
        logging.info(f"💬 Resposta da IA: {resposta_ia}")
        # 4. Extração segura da palavra-chave (Lida com pontos, espaços e quebras de linha que LLMs costumam adicionar)
        regime = resposta_ia.split(".")[0].split(" ")[0].strip().upper()
        
        # 5. Validação de segurança (Caso a IA "alucine" uma palavra que não existe no protocolo)
        if regime not in ["BULLISH", "BEARISH", "NEUTRAL"]:
            logging.warning(f"IA retornou regime inválido '{regime}'. Forçando proteção: NEUTRAL.")
            regime = "NEUTRAL"
            
        logging.info(f"👔 Veredito do Estrategista para {symbol}: {regime}")
            
        # 6. Salva o regime na memória local para o robô matemático (TechTrader) ler posteriormente
        file_path = f"data/{symbol}_regime.txt"
        
        # Garante que a pasta data/ existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(regime)
            
        return regime