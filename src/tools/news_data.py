import urllib.request
import xml.etree.ElementTree as ET
import logging

class NewsDataTool:
    def __init__(self):
        # Usamos o feed RSS do CoinTelegraph (gratuito e atualizado em tempo real)
        self.rss_url = "https://cointelegraph.com/rss"

    def get_crypto_news(self, symbol: str) -> str:
        """Busca as últimas notícias e filtra pelo ativo desejado."""
        # Extrai a moeda base (ex: "BTCUSDT" -> "BTC")
        coin = symbol.replace("USDT", "")
        
        try:
            # Faz a requisição disfarçada de navegador para não ser bloqueado
            req = urllib.request.Request(self.rss_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()
                
            root = ET.fromstring(xml_data)
            headlines = []
            
            for item in root.findall('./channel/item'):
                title = item.find('title').text
                
                # Para ser assertivo, tenta encontrar o nome da moeda na manchete.
                # Se for BTC, pega quase tudo, pois dita o mercado.
                if coin in title.upper() or coin == "BTC":
                    headlines.append(f"- {title}")
                
                # Pega no máximo as 5 notícias mais recentes para não poluir o prompt
                if len(headlines) >= 5:
                    break
                    
            if not headlines:
                return "Nenhuma notícia relevante de grande impacto nas últimas horas."
                
            return "\n".join(headlines)
            
        except Exception as e:
            logging.error(f"Erro ao buscar notícias no CoinTelegraph: {e}")
            return "Feed de notícias temporariamente indisponível."