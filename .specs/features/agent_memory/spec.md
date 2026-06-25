# Especificação: Memória do agente

## Objetivo
Permitir que o agente armazene e recupere decisões anteriores para enriquecer o contexto do próximo ciclo.

## Requisitos
- Armazenar decisões e resultados em SQLite.
- Recuperar os registros mais recentes para o símbolo ou contexto atual.
- Manter a operação simples e compatível com o modo dry run.

## Critérios de aceitação
- Uma decisão pode ser salva e lida posteriormente.
- O fluxo não depende de serviços externos.
- A memória é facilmente acessível pelo orquestrador.
