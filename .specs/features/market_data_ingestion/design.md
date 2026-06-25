# Design: Ingestão incremental de dados

## Componentes
- MarketDataService: orquestra a leitura e persistência dos dados.
- SQLite: armazena o histórico de candles e a última data processada.
- Adapter de dados: encapsula a obtenção dos dados externos, que pode ser substituído futuramente.

## Fluxo
1. O serviço consulta a última vela para o símbolo informado.
2. Se não houver dados, usa uma carga inicial padrão.
3. Se houver dados, busca apenas as velas posteriores à última data.
4. Insere as novas velas e retorna o resultado do processamento.
