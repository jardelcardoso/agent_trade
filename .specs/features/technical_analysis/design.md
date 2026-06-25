# Design: Análise técnica básica

## Componentes
- TechnicalAnalysisService: lê os candles do banco e calcula indicadores simples.
- MarketDataService: fornece os dados persistidos.
- Orchestrator: usa o resultado da análise para decidir o próximo passo.

## Fluxo
1. O serviço busca os candles mais recentes do símbolo.
2. Calcula indicadores simples como retorno e média móvel.
3. Retorna um sinal, por exemplo, `buy`, `sell` ou `hold`.
