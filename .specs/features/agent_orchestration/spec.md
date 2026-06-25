# Especificação: Orquestração do agente

## Objetivo
Permitir que o agente execute um ciclo simples que combine coleta de dados, validação de risco e registro da decisão em modo dry run.

## Requisitos
- O orquestrador deve usar o serviço de dados de mercado.
- O orquestrador deve usar o gestor de risco.
- O ciclo deve ser executável sem depender de uma corretora real.

## Critérios de aceitação
- Um ciclo gera um registro de mercado e um registro de trade simulado.
- O resultado do ciclo é retornado de forma clara para o ponto de entrada.
