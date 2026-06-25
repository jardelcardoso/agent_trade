# Agent Trade

Este projeto implementa uma base para um agente de trading com execução em modo dry run, persistência local em SQLite e um ciclo simplificado de análise + decisão.

## Estrutura

- .specs/ - documentação de projeto e arquitetura
- config/ - configuração do agente e do modo dry run
- src/ - código-fonte principal
- tests/ - testes automatizados

## Como começar

1. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Instale as dependências:
   ```bash
   python -m pip install -e .
   ```
3. Execute o ponto de entrada principal:
   ```bash
   python main.py
   ```

## Modo dry run

O projeto roda preferencialmente com `execution_mode.dry_run: true` em [config/settings.yaml](config/settings.yaml). Nesse modo, as ordens são registradas localmente em SQLite em vez de serem enviadas para uma corretora real.

## Arquivos principais

- [config/settings.yaml](config/settings.yaml) - configuração do comportamento do agente
- [main.py](main.py) - ponto de entrada
- [src/agent/orchestrator.py](src/agent/orchestrator.py) - ciclo principal do agente
- [src/risk/risk_manager.py](src/risk/risk_manager.py) - validação e registro de ordens
