import urllib.request
import json
import logging

class SentimentTool:
    def __init__(self):
        self.api_url = "https://api.alternative.me/fng/?limit=1"

    def get_fear_and_greed(self) -> str:
        """Busca o Crypto Fear & Greed Index na API pública."""
        try:
            req = urllib.request.Request(self.api_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                value = data['data'][0]['value']
                classification = data['data'][0]['value_classification']
                return f"Índice de Medo e Ganância: {value}/100 ({classification})"
        except Exception as e:
            logging.error(f"Erro ao buscar sentimento: {e}")
            return "Índice de Medo e Ganância: Indisponível no momento."