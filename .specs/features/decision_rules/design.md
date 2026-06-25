# Design: Prompts e regras de decisão

## Componentes
- DecisionPolicy: encapsula as regras de decisão em formato simples.
- Orchestrator: usa a política para decidir entre buy, sell e hold.
- Memory e análise técnica: fornecem contexto para a política.

## Fluxo
1. O orquestrador coleta sinal, contexto de memória e estado do ciclo.
2. A política aplica regras simples para gerar uma decisão.
3. O resultado é usado pelo gestor de risco e persistido como decisão do agente.
