# Tarefas da Funcionalidade: Carga Incremental de Dados

## 1. Criar o módulo de serviço de ingestão
- [ ] Criar o arquivo src/tools/market_data.py com uma classe responsável por orquestrar a carga incremental.
- [ ] Definir um método para localizar o último timestamp registrado em market_data.
- [ ] Definir um método para iniciar a carga a partir de um ponto inicial configurado quando não houver dados.

## 2. Implementar persistência no SQLite
- [ ] Criar a função para salvar candles no banco sem duplicar registros.
- [ ] Garantir que cada registro seja persistido com os campos OHLCV e timestamp.
- [ ] Adicionar testes para verificar a idempotência da escrita.

## 3. Implementar o adaptador de dados
- [ ] Definir uma interface abstrata para o provider de dados.
- [ ] Criar uma implementação stub para permitir testes sem dependência externa.
- [ ] Integrar o provider ao fluxo de carga incremental.

## 4. Validar o fluxo completo
- [ ] Criar um teste para o caso de banco vazio.
- [ ] Criar um teste para o caso de reexecução sem duplicação.
- [ ] Executar os testes e confirmar o comportamento esperado.

## Critérios de Verificação
- O sistema lê o último timestamp do banco.
- A carga é limitada ao intervalo faltante.
- Os dados são persistidos corretamente sem duplicação.
- Os testes automatizados passam.
