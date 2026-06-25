# Especificação: Integração do broker no orquestrador

## Objetivo
Permitir que o orquestrador use um broker concreto via a interface definida, mantendo o fluxo compatível com dry run.

## Requisitos
- O orquestrador deve aceitar um broker opcional.
- A execução de trade deve delegar para o broker.
- O fluxo deve continuar a funcionar sem configuração externa.

## Critérios de aceitação
- O orquestrador executa uma ordem através do broker fornecido.
- Sem broker explícito, o modo dry run é usado por padrão.
- O comportamento é coberto por testes.
