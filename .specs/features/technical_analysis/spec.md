# Especificação: Análise técnica básica

## Objetivo
Adicionar uma camada simples de análise técnica para produzir um sinal a partir dos dados persistidos de mercado.

## Requisitos
- Ler candles salvos em SQLite.
- Calcular indicadores simples como retorno e média móvel.
- Retornar um sinal de decisão para o orquestrador.

## Critérios de aceitação
- O serviço consegue calcular um sinal a partir de candles armazenados.
- O resultado é determinístico para um conjunto de dados conhecido.
- O fluxo pode ser testado sem acesso externo.
