# Design da Funcionalidade: Carga Incremental de Dados

## Visão Geral
A funcionalidade será implementada como um fluxo simples e modular no pacote src/tools, responsável por:
1. consultar o último timestamp presente em market_data;
2. calcular o intervalo de dados a carregar;
3. buscar os candles faltantes;
4. persistir os registros no banco SQLite sem duplicação.

## Arquitetura Proposta

### Componentes
- MarketDataService: ponto de entrada da funcionalidade, orquestra a leitura e escrita.
- DataProviderPort: interface abstrata para buscar candles de uma corretora ou fonte externa.
- SQLiteMarketStore: implementação concreta para ler/escrever no banco via SQLAlchemy.
- ConfigLoader: leitura do intervalo e parâmetros básicos de configuração.

### Fluxo
1. O serviço consulta o último registro de market_data.
2. Se existir, usa esse timestamp como base para a próxima janela.
3. Se não existir, inicia a carga a partir de um valor padrão configurado.
4. O provider busca os candles no range desejado.
5. Os registros são convertidos para o modelo ORM e persistidos.
6. O processo termina sem duplicar dados já salvos.

## Estruturas de Dados

### Modelo de mercado
Campos esperados:
- symbol
- timestamp
- open
- high
- low
- close
- volume

### Interface do provider
```python
class DataProviderPort:
    def fetch_candles(self, symbol: str, start_time, end_time, interval: str):
        raise NotImplementedError
```

## Decisões de Implementação
- O banco continua sendo a fonte de verdade para o estado incremental.
- O processo deve ser idempotente, verificando se o timestamp já existe antes de inserir.
- A implementação inicial pode usar um provider stub ou mock para permitir testes sem API externa.
- A lógica de intervalo deve ser centralizada para facilitar adaptação futura a outros brokers.

## Testes Planejados
- Banco vazio: deve carregar o primeiro lote de dados.
- Banco com registros: deve carregar apenas o novo intervalo.
- Reexecução: não deve duplicar registros.
- Falha de provider: deve retornar erro controlado sem corromper o banco.

## Critérios de Aceitação
- O fluxo consegue persistir dados incrementais em SQLite.
- O sistema não reenvia registros já existentes.
- A lógica fica isolada o suficiente para evoluir para integração real com corretoras.
