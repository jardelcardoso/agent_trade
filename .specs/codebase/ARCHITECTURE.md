# Arquitetura

O projeto é organizado em quatro blocos principais:
- Agent: orquestração do ciclo ReAct.
- Tools: coleta e análise de dados.
- Risk: validação da operação antes de execução.
- Brokers: adaptadores para corretoras.

A execução padrão usa dry run, registrando ordens simuladas em SQLite.
