# Design: Integração do broker no orquestrador

## Componentes
- Orchestrator: recebe um broker opcional no construtor.
- DryRunBroker: implementação padrão quando nenhum broker é fornecido.
- RiskManager: continua responsável pela decisão de risco e pela validação do fluxo.

## Fluxo
1. O orquestrador cria ou recebe um broker.
2. O broker é usado para executar a ordem após a decisão.
3. O resultado é retornado como parte do ciclo do agente.
