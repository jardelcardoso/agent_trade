# Agent Trade

**Visão:** Criar um agente de trading autónomo em modo dry run, com análise técnica, orquestração por IA e persistência local em SQLite.
**Para:** Desenvolvedores e traders sistemáticos interessados em automação e validação de estratégias.
**Resolve:** Permitir validação segura de decisões de trading antes de qualquer execução real.

## Objetivos

- Implementar uma base funcional do agente com ciclo de coleta, análise, decisão e registro em SQLite.
- Garantir que o fluxo principal rode em modo dry run sem depender de corretora real.
- Proporcionar uma estrutura modular que possa evoluir para integração com outros brokers.

## Tech Stack

**Core:**
- Linguagem: Python 3.10+
- Banco de Dados: SQLite + SQLAlchemy
- Configuração: YAML

**Dependências-chave:**
- pandas
- PyYAML
- pytest
- SQLAlchemy

## Escopo

**v1 inclui:**
- Estrutura de pacotes e arquivos de configuração
- Banco de dados local inicial
- Ponto de entrada do agente em modo dry run
- Módulos base para orchestrator, ferramentas, risco e brokers

**Explicitamente fora de escopo:**
- Execução com dinheiro real
- Interface gráfica
- Integração com múltiplos brokers na fase inicial

## Restrições

- Prazo: MVP inicial
- Técnicas: arquitetura modular e isolamento de responsabilidades
- Recursos: foco em execução local e validação segura
