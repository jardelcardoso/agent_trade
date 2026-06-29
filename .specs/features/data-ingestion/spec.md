# Especificação da Funcionalidade: Carga Incremental de Dados

## Objetivo
Implementar uma rotina de ingestão de dados de mercado que consulte o banco SQLite, identifique o último timestamp registrado e carregue apenas os candles faltantes até o momento atual.

## Contexto
Conforme o PRD, a aplicação deve evitar chamadas desnecessárias à API da corretora e respeitar limites de taxa, usando o banco local como fonte de verdade para a última posição conhecida.

## Requisitos

### Funcionais
- O sistema deve consultar a tabela market_data e localizar o último timestamp disponível.
- Se não houver registros, deve iniciar a carga a partir de um intervalo configurado.
- Deve solicitar apenas os dados mais recentes que ainda não foram persistidos.
- Os dados carregados devem ser salvos em market_data com os campos OHLCV.
- A rotina deve ser idempotente, evitando duplicação de registros.

### Não Funcionais
- Deve usar SQLite e SQLAlchemy.
- Deve ser implementável sem depender de execução real de ordens.
- Deve permitir futura troca de broker com mínimas mudanças.

## Critérios de Aceitação
- Uma execução com banco vazio cria o primeiro lote de dados.
- Uma execução subsequente não repete os registros já existentes.
- O fluxo consegue terminar sem erro em modo dry run.

## Restrições
- A integração com a API da corretora é opcional nesta fase; a implementação deve ser compatível com um adaptador futuro.
- Não devem existir chaves sensíveis no código-fonte.
