# Especificação: Execução de ordens em dry run

## Objetivo
Permitir que o agente valide uma ordem e registre a execução em modo simulado sem depender de uma corretora real.

## Requisitos
- Ler configuração de execução do arquivo YAML.
- Se dry_run estiver ativo, registrar a ordem em SQLite com status de simulação.
- Manter a operação isolada da camada de broker real.

## Critérios de aceitação
- Uma ordem simulada gera um registro em banco de dados.
- O fluxo não exige conexão externa à corretora.
- A configuração pode ser alterada sem mudar o código.
