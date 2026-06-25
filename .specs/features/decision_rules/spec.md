# Especificação: Prompts e regras de decisão do agente

## Objetivo
Adicionar uma camada simples de regras de decisão para transformar a análise técnica e o contexto da memória em uma ação coerente.

## Requisitos
- Definir regras textuais e estruturadas para orientar a decisão.
- Aplicar essas regras no orquestrador.
- Manter o comportamento determinístico e compatível com dry run.

## Critérios de aceitação
- O orquestrador produz uma decisão baseada em sinal, contexto e regras.
- A decisão pode ser testada sem depender de LLM externa.
