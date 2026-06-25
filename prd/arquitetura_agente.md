Arquitetura do Agente Autônomo de TradingEste documento define a estrutura do software baseada no padrão ReAct (Reason + Act) e Arquitetura Hexagonal (Ports and Adapters). O objetivo principal é isolar a IA (Orquestradora) do código Python (Motor de Risco e Execução).1. Decisões Estratégicas de EngenhariaBaseado nos requisitos do sistema, estabelecemos três pilares técnicos fundamentais:Armazenamento em SQLite: O banco trading_db.sqlite será a fonte única de verdade (Single Source of Truth) tanto para o histórico de preços (OHLCV) quanto para o registo das ordens e logs do agente.Carga Incremental de Dados: O sistema não baixará o histórico completo a cada ciclo. A ferramenta de extração sempre consultará o SQLite para encontrar a data/hora da última "vela" salva e solicitará à corretora apenas os dados desse momento até ao presente.Execução em Modo Dry Run: O sistema operará primariamente com a flag dry_run: True. Neste modo, o pipeline de dados, a IA e o cálculo de risco funcionam a 100% da sua capacidade. No entanto, no último milissegundo, a ordem de compra/venda real é bloqueada e registada apenas como um Log Simulado no banco de dados.2. Diagrama de Arquitetura (Fluxo de Dados)O diagrama abaixo ilustra como os componentes interagem com as novas regras de Dry Run e SQLite.+-----------------------------------------------------------------------------------+
|                                 RUNTIME PRINCIPAL (Python)                        |
|                                     (Loop de Execução)                            |
+-----------------------------------------------------------------------------------+
        |                               ^                                 |
        v                               |                                 v
+------------------+           +------------------+              +------------------+
|   1. O CÉREBRO   |   Pede    |   2. AS TOOLS    |   Entrega    | 3. O GUARDA-COSTAS |
|     (LLM / IA)   | --------> | (Funções Python) | -----------> | (Gerenciador Risco)|
|                  |   Dados   |                  |   Decisão    |                  |
| - Prompts Base   |           | - Baixar Dados   |   de Trade   | - Valida Saldo     |
| - Memória Curta  | <-------- | - Analisar RSI   |              | - Calcula Lote     |
| - Decisão Lógica | Entregou  | - Ler Notícias   |              | - Trava Perdas     |
+------------------+ Resumo    +------------------+              +------------------+
                                  |    ^                                  |
               Salva/Lê Incremental    | Lê Última Data                   | Ordem Validada
                                  v    |                                  v
                             +------------------+                +------------------+
                             | BANCO DE DADOS   |                |  4. ADAPTADORES  |
                             |     (SQLite)     |                | (Interfaces API) |
                             +------------------+                +------------------+
                                                                   |              |
                                                      [Dry Run Ativo?]         [Dry Run False]
                                                                   |              |
                                                                   v              v
                                                       Gera Log da Ordem     +---------+
                                                       e Salva no SQLite     | BINANCE |
                                                                             | (Real)  |
                                                                             +---------+

3. Estrutura de Diretórios e ArquivosEsta é a árvore de pastas do seu projeto Python atualizada:agent_trading/
│
├── .env                    # Variáveis de ambiente (Chaves API da Binance Live)
├── requirements.txt        # Lista de dependências (pandas, openai, python-binance, sqlalchemy)
├── main.py                 # Ponto de entrada do sistema. Loop infinito.
│
├── config/                 # Configurações globais e Prompts
│   ├── settings.yaml       # Configuração de Risco e a flag 'dry_run: True'
│   └── agent_prompts.py    # Textos que definem o 'mandato' da IA (Day, Swing, etc.)
│
├── data/                   # Armazenamento Local
│   └── trading_db.sqlite   # Banco de dados principal contendo 3 tabelas:
│                           # 1. market_data (Histórico incremental OHLCV)
│                           # 2. trades_log (Registo de ordens Dry Run ou Reais)
│                           # 3. agent_memory (Memória de decisões do LLM)
│
└── src/                    # Código Fonte da Aplicação
    │
    ├── agent/              # O "Cérebro"
    │   ├── __init__.py
    │   ├── orchestrator.py # Inicializa o LLM e coordena o ciclo ReAct
    │   └── memory.py       # Gere o contexto enviado no prompt
    │
    ├── tools/              # As "Mãos" e "Olhos"
    │   ├── __init__.py
    │   ├── market_data.py  # Consulta o SQLite pelo último registo e faz extração incremental
    │   └── tech_analysis.py# Calcula indicadores técnicos usando os dados do SQLite
    │
    ├── risk/               # O "Guarda-Costas"
    │   ├── __init__.py
    │   └── risk_manager.py # Valida o trade contra settings.yaml. Avalia a flag 'dry_run'.
    │
    └── brokers/            # Os "Adaptadores"
        ├── __init__.py
        ├── base_broker.py  # Interface padrão de envio de ordem
        └── binance.py      # Conector real da Binance. Executa de facto se dry_run=False

4. Detalhamento dos Componentes Chave Atualizadosconfig/settings.yamlAqui nós ativaremos o modo simulado de forma global. Exemplo do ficheiro:execution_mode:
  dry_run: true                 # Se verdadeiro, NÃO envia a ordem para a corretora
  timeframe: "15m"              # Resolução dos dados

risk_management:
  risk_per_trade_percent: 1.0   # % da banca a arriscar
  max_daily_drawdown: 5.0       # Perda máxima diária aceitável

src/tools/market_data.py (Carga Incremental)A ferramenta de ingestão agora possui inteligência de banco de dados. O pseudo-código do fluxo será:Conecta no trading_db.sqlite.Executa SELECT MAX(timestamp) FROM market_data WHERE symbol = 'BTCUSDT'.Se retornar Vazio, busca as últimas 1000 velas da Binance (Carga Inicial).Se retornar uma Data (ex: Hoje às 10:00), busca na Binance apenas as velas de 10:00 até Agora.Faz o Insert/Update no banco.src/risk/risk_manager.py (O Ponto do Dry Run)Após a IA decidir comprar, a ordem passa por aqui. O código fará a seguinte validação lógica:if configuracao["execution_mode"]["dry_run"]:
    log_msg = f"[DRY RUN] Executando ordem FANTASMA: COMPRA de 0.015 BTCUSDT a $65.000. Stop em $63.000."
    salvar_no_sqlite("trades_log", log_msg)
    print(log_msg)
    return "Ordem simulada executada com sucesso"
else:
    # Chama o broker de verdade
    broker.enviar_ordem("COMPRA", 0.015, "BTCUSDT")

