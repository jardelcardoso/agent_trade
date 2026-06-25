# Design: Orquestração do agente

## Componentes
- Orchestrator: coordena o ciclo ReAct simplificado.
- MarketDataService: oferece dados simulados para o ciclo.
- RiskManager: valida a ordem antes do registro final.

## Fluxo
1. O orquestrador prepara um candle simples.
2. O serviço de mercado persiste o candle.
3. O gestor de risco registra a ordem como dry run.
4. O orquestrador retorna um resumo do ciclo.
