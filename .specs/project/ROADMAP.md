# Roadmap do Projeto

## Fase 1 - Fundação do MVP
- Finalizar a estrutura base do projeto e os arquivos de configuração.
- Garantir a criação e inicialização do banco SQLite local.
- Validar o fluxo principal em modo dry run sem dependência de corretora real.

## Fase 2 - Coleta e Análise
- Implementar a ingestão incremental de dados de mercado.
- Criar ferramentas para leitura de candles e cálculo de indicadores técnicos.
- Produzir resumos simples para o LLM com base nos dados locais.

## Fase 3 - Decisão e Risco
- Implementar um orquestrador ReAct com decisão textual clara.
- Adicionar gestão de risco determinística e validação de tamanho de posição.
- Registrar ordens simuladas no SQLite com justificativa e flag de dry run.

## Fase 4 - Preparação para Evolução
- Isolar a interface do broker para futuras integrações.
- Documentar pontos de extensão para Binance e outros mercados.
- Preparar o projeto para testes automatizados de fluxo e persistência.
