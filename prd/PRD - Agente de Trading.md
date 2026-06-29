# **Documento de Requisitos do Produto (PRD)**

## **Projeto: Agente Autónomo de Trading (Agent Trade)**

### **1\. Visão Geral do Produto**

O **Agent Trade** é um sistema de trading automatizado baseado em Inteligência Artificial, construído sobre a arquitetura ReAct (Reasoning and Acting). Ao contrário de robôs de trading tradicionais baseados em regras rígidas (if/else), este sistema utiliza um Large Language Model (LLM) como "Cérebro" orquestrador. A IA avalia resumos de mercado, delibera sobre o contexto e aciona ferramentas (Tools) desenvolvidas em Python para executar ações rigorosamente controladas por um gestor de risco determinístico.

### **2\. Objetivos**

* **Autonomia com Segurança:** Permitir que a IA tome decisões de compra/venda baseadas em análise técnica, sem nunca lhe dar controlo direto sobre o envio de ordens ou cálculos financeiros brutos.  
* **Validação Sem Risco (Dry Run):** Possibilitar a execução contínua do agente em ambiente de produção simulado (Dry Run), registando decisões em base de dados local para validação de estratégias antes de arriscar capital real.  
* **Escalabilidade e Agnosticismo:** Garantir que o sistema (via Arquitetura Hexagonal) possa transitar da corretora Binance (criptomoedas) para a B3 (mercado tradicional) no futuro com alterações mínimas no código.

### **3\. Público-Alvo**

* Desenvolvedores e Engenheiros de Dados interessados em Finanças Quantitativas (*Quant Finance*).  
* Traders sistemáticos que desejam introduzir análise de contexto via LLMs nas suas operações diárias.

### **4\. Escopo do Projeto (Fase 1 \- MVP)**

**Dentro do Escopo:**

* Integração com a API da Binance (Spot Market).  
* Banco de dados local via SQLite (trading\_db.sqlite) com tabelas isoladas para dados de mercado e registo de trades.  
* Sistema de Ingestão Incremental de Dados (evitando bloqueios de API/Rate Limits).  
* Orquestrador de IA implementado via API da OpenAI (ex: gpt-4o).  
* Execução puramente em modo *Dry Run* (Simulação).  
* Gestão de risco fixa configurada via YAML (settings.yaml).

**Fora do Escopo (Fase 1):**

* Interface Gráfica de Utilizador (UI/Front-end). O sistema rodará em terminal/background.  
* High-Frequency Trading (HFT) ou arbitragem de milissegundos.  
* Execução de ordens com dinheiro real na Fase 1 (proteção obrigatória via *Dry Run*).  
* Conexão com a B3.

### **5\. Requisitos Funcionais (RF)**

* **RF01 \- Carga Incremental:** O sistema deve consultar o SQLite pelo último *timestamp* registado e solicitar à corretora apenas os dados das velas (OHLCV) ausentes desde esse ponto até ao momento atual.  
* **RF02 \- Abstração de Análise:** O sistema deve possuir uma *Tool* (TechAnalysisTool) que processa os dados do SQLite, calcula indicadores (ex: RSI, MACD) e devolve um resumo textual simples para o LLM.  
* **RF03 \- Orquestração ReAct:** O AgentOrchestrator deve invocar a OpenAI, fornecendo o resumo técnico no *prompt* de sistema e aguardando uma decisão textual clara (ex: COMPRAR, VENDER, AGUARDAR).  
* **RF04 \- Gestão de Risco Determinística:** Todas as decisões da IA que envolvam execução devem passar pelo RiskManager. Este módulo deve calcular o tamanho do lote baseado num limite percentual máximo de risco e bloquear a operação se violar as regras.  
* **RF05 \- Execução Simulada (Dry Run):** Quando a flag dry\_run estiver ativa nas configurações, a ordem final deve ser intercetada e gravada apenas na tabela trades\_log do SQLite, sem comunicação de compra com a API da corretora.

### **6\. Requisitos Não-Funcionais (RNF)**

* **RNF01 \- Arquitetura Hexagonal:** O sistema deve manter isolamento estrito entre O Cérebro (LLM), as Ferramentas (Tools), o Risco (Risk Manager) e os Adaptadores (Brokers).  
* **RNF02 \- Armazenamento Local Leve:** Utilização exclusiva de SQLite via SQLAlchemy ORM para facilitar a portabilidade do projeto.  
* **RNF03 \- Segurança de Credenciais:** Nenhuma chave de API (OpenAI, Binance) pode existir no código-fonte, sendo a sua leitura feita obrigatoriamente através de variáveis de ambiente (.env).  
* **RNF04 \- Configuração Dinâmica:** Parâmetros de *timeframe* e limites de risco devem ser lidos de um ficheiro config/settings.yaml.

### **7\. Casos de Uso Principais**

1. **O Agente decide Aguardar:** O *loop* principal acorda o Orquestrador \-\> A Tool de Análise lê o SQLite \-\> O mercado está lateralizado \-\> A IA recebe o resumo e decide não operar \-\> O ciclo encerra.  
2. **O Agente decide Comprar (Dry Run):** O Orquestrador analisa o resumo \-\> RSI está sobrevendido e em tendência de alta \-\> IA decide "COMPRAR" \-\> RiskManager valida o lote em 1% do capital \-\> RiskManager vê que é *Dry Run* \-\> Grava a ordem fantasma no SQLite trades\_log \-\> O ciclo encerra.

### **8\. Estrutura de Diretórios e Arquivos**

O projeto deve obedecer rigorosamente à seguinte estrutura de pastas e ficheiros, separando as responsabilidades conforme a arquitetura proposta:

agent\_trading/  
│  
├── .env                    \# Variáveis de ambiente (Chaves API da Binance Live, OpenAI)  
├── requirements.txt        \# Lista de dependências (pandas, openai, python-binance, sqlalchemy)  
├── main.py                 \# Ponto de entrada do sistema. Loop infinito.  
├── database.py             \# Script para criar as tabelas e gerir a ligação com SQLite.  
│  
├── config/                 \# Configurações globais e Prompts  
│   ├── settings.yaml       \# Configuração de Risco e a flag 'dry\_run: True'  
│   └── agent\_prompts.py    \# Textos que definem o 'mandato' da IA (Day, Swing, etc.)  
│  
├── data/                   \# Armazenamento Local  
│   └── trading\_db.sqlite   \# Banco de dados principal contendo 3 tabelas:  
│                           \# 1\. market\_data (Histórico incremental OHLCV)  
│                           \# 2\. trades\_log (Registo de ordens Dry Run ou Reais)  
│                           \# 3\. agent\_memory (Memória de decisões do LLM)  
│  
└── src/                    \# Código Fonte da Aplicação  
    │  
    ├── agent/              \# O "Cérebro"  
    │   ├── \_\_init\_\_.py  
    │   ├── orchestrator.py \# Inicializa o LLM e coordena o ciclo ReAct  
    │   └── memory.py       \# Gere o contexto enviado no prompt  
    │  
    ├── tools/              \# As "Mãos" e "Olhos"  
    │   ├── \_\_init\_\_.py  
    │   ├── market\_data.py  \# Consulta o SQLite pelo último registo e faz extração incremental  
    │   └── tech\_analysis.py\# Calcula indicadores técnicos usando os dados do SQLite  
    │  
    ├── risk/               \# O "Guarda-Costas"  
    │   ├── \_\_init\_\_.py  
    │   └── risk\_manager.py \# Valida o trade contra settings.yaml. Avalia a flag 'dry\_run'.  
    │  
    └── brokers/            \# Os "Adaptadores"  
        ├── \_\_init\_\_.py  
        ├── base\_broker.py  \# Interface padrão de envio de ordem  
        └── binance.py      \# Conector real da Binance. Executa de facto se dry\_run=False

### **9\. Métricas de Sucesso**

* O sistema consegue rodar ininterruptamente por 7 dias num servidor, alimentando o banco SQLite de forma incremental sem ultrapassar limites de taxa (*rate limits*) da Binance.  
* O *log* do SQLite (trades\_log) reflete corretamente as decisões da IA, contendo o preço exato, ação, justificação gerada pelo LLM e indicador de *Dry Run*.