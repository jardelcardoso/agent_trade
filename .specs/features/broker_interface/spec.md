# Especificação: Interface para brokers reais

## Objetivo
Definir uma abstração simples para envio de ordens que permita futuramente integrar corretoras reais sem alterar o restante do sistema.

## Requisitos
- Criar uma interface base para execução de ordens.
- Permitir uma implementação fake para modo dry run.
- Manter o restante do sistema independente da implementação concreta.

## Critérios de aceitação
- O orquestrador pode receber um broker concreto sem mudar a lógica principal.
- O fluxo dry run é compatível com a interface.
- O comportamento pode ser testado isoladamente.
