# Design: Memória do agente

## Componentes
- AgentMemory: camada simples de persistência para eventos do agente.
- SQLite: armazenamento local das entradas de memória.
- Orchestrator: usa a memória para compor um contexto resumido.

## Fluxo
1. O orquestrador registra uma decisão com status e contexto.
2. A memória salva o registro em tabela local.
3. O próximo ciclo consulta os últimos registros para complementar o contexto.
