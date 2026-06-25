# Design: Integração da memória ao contexto de decisão

## Componentes
- AgentMemory: fornece decisões recentes por símbolo.
- Orchestrator: consulta a memória antes de analisar o mercado.
- Resultado do ciclo: inclui um resumo do contexto de memória.

## Fluxo
1. O orquestrador consulta a memória recente do símbolo.
2. Monta um resumo simples com as últimas decisões.
3. Usa esse resumo para complementar a decisão atual e retornar o contexto.
