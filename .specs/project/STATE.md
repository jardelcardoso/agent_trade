# Estado Atual

- Projeto inicializado com estrutura base.
- Arquitetura atual segue o modelo ReAct com separação entre agente, ferramentas, risco e adaptadores.
- Execução padrão é dry run.

## Próximos passos
1. Implementar fluxo de dados incremental.
2. Expandir o orquestrador para usar a gestão de risco.
3. Adicionar testes e validações adicionais.

## Última atualização
- Implementada a funcionalidade de execução dry run com registro em SQLite.
- Implementada a ingestão incremental de dados de mercado com persistência em SQLite.
- Implementado o orquestrador do agente para executar um ciclo simples de dados + risco.
- Implementada a memória do agente com persistência local em SQLite.
- Implementada a análise técnica básica e integrada ao ciclo do agente.
- Integrada a memória ao contexto de decisão do orquestrador.
- Adicionadas regras de decisão simples para orientar a escolha do próximo trade.
- Definida uma interface base para brokers e um adaptador de dry run.
- Integrado o broker ao ciclo do orquestrador via interface.
- Atualizada a documentação de execução e configuração com instruções de uso.
- Adicionados testes para validar os fluxos simulados.
