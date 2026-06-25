# Especificação: Ingestão incremental de dados de mercado

## Objetivo
Implementar a coleta incremental de candles de mercado usando SQLite como fonte de verdade e evitar recarregar o histórico completo a cada execução.

## Requisitos
- Consultar o banco SQLite para encontrar a última vela salva por símbolo.
- Se não existir histórico, realizar uma carga inicial.
- Se existir histórico, buscar apenas o intervalo novo até o presente.
- Persistir os dados em uma tabela de mercado.

## Critérios de aceitação
- O fluxo consegue inicializar o banco quando não há dados.
- O fluxo consegue identificar o ponto de corte e salvar apenas os dados novos.
- A lógica é testável sem depender de uma corretora real.
