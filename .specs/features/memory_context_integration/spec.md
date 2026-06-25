# Especificação: Integração da memória ao contexto de decisão

## Objetivo
Incorporar os registros recentes de memória ao contexto do ciclo de decisão do agente.

## Requisitos
- O orquestrador deve recuperar decisões recentes da memória.
- O contexto recuperado deve influenciar o resultado do ciclo.
- O comportamento deve continuar compatível com o modo dry run.

## Critérios de aceitação
- O ciclo retorna um contexto contendo as decisões recentes.
- O fluxo é testável sem dependência externa.
