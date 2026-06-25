# Design: Execução dry run

## Componentes
- RiskManager: encapsula a validação da ordem.
- Configuração YAML: define se a execução deve ser dry run.
- Banco SQLite: armazena o log das ordens simuladas.

## Fluxo
1. O orquestrador solicita uma validação de ordem.
2. O RiskManager lê as configurações.
3. Se dry_run for verdadeiro, cria um registro em `trades_log`.
4. Retorna um resumo da decisão para o restante do pipeline.
