# Design: Interface para brokers reais

## Componentes
- BrokerProtocol: define o contrato de envio de ordens.
- DryRunBroker: implementação padrão para o modo simulado.
- Orchestrator: depende da interface, não da implementação concreta.

## Fluxo
1. O orquestrador escolhe um broker.
2. O broker recebe a ordem e a processa.
3. Em dry run, a ordem é registrada localmente; em modo real, a implementação pode enviar para uma corretora.
