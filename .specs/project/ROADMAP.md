# Roadmap

## Fase 1 - Fundação
- [x] Definir arquitetura inicial baseada em ReAct e portas/adaptadores.
- [x] Criar estrutura de diretórios base para agente, ferramentas, risco e brokers.
- [x] Definir ambiente Python inicial com dependências mínimas.

## Fase 2 - Núcleo do agente
- [x] Implementar ingestão incremental de dados de mercado com persistência em SQLite.
- [x] Implementar gestão de risco com execução em modo dry run.
- [x] Implementar orquestração do agente para um ciclo simples de dados + risco.
- [x] Implementar memória local do agente para registrar decisões anteriores.

## Fase 3 - Análise e decisão
- [x] Implementar análise técnica básica sobre os dados persistidos.
- [x] Integrar a memória ao contexto do ciclo de decisão.
- [x] Adicionar prompts e regras de decisão do agente.

## Fase 4 - Integração e operação
- [x] Definir interface para brokers reais.
- [x] Integrar o broker ao ciclo do orquestrador.
- [x] Documentar execução, configuração e uso em modo dry run.
