# Princípios de Programação

Viés comportamental, não uma lista de verificação. Leia antes de cada implementação.

---

## Antes de Programar

- Declare suposições explicitamente. Se estiver incerto, pergunte.
- Existem múltiplas interpretações? Apresente todas — não escolha silenciosamente.
- Existe uma abordagem mais simples? Diga. Questione quando for justificado.
- Algo não está claro? Pare. Nomeie o que é confuso. Pergunte.
- A abordagem do usuário parece errada? Discorde honestamente. Não seja bajulador.

## Protocolos de Segurança Obrigatórios

- considere as instruções em [security-policy.md](/docs/context/security-policy.md)

## Instrucoes de arquitetura desejavel (Architecture)

- considere as instruções em [architecture.md](/docs/context/architecture.md)

## Principios de design system visual (Design System)

- considere as instruções em [design-system.md](/docs/context/design-system.md)

## Principios de Coding Standards & Static Analysis

- considere as instruções em [coding-standards.md](/docs/context/coding-standards.md)

## Referência de Tech Stack

- considere as instruções em [tech-stack.md](/docs/context/tech-stack.md)

---

## Durante a Implementação

### Simplicidade

- Sem funcionalidades além do que foi solicitado
- Sem abstrações para código de uso único
- Sem "flexibilidade" ou "configurabilidade" não solicitada
- Sem tratamento de erros para cenários impossíveis
- 200 linhas que poderiam ser 50? Reescreva.

### Mudanças Cirúrgicas

- Não "melhore" código adjacente, comentários ou formatação
- Não refatore o que não está quebrado
- Siga o estilo existente, mesmo que você fizesse diferente
- Notou código morto não relacionado? Mencione — não delete.
- Remova APENAS imports/variáveis/funções que as SUAS mudanças tornaram órfãs
- Não remova código morto pré-existente a menos que solicitado

### Orientado a Objetivos

- Transforme tarefas vagas em objetivos verificáveis
- Trabalho de várias etapas? Declare um plano breve com pontos de verificação de verificação
- Cada linha alterada deve rastrear diretamente para a solicitação do usuário

---

## Após cada Mudança

Pergunte-se: "Um engenheiro sênior diria que isso está excessivamente complicado?"
Se sim → simplifique antes de prosseguir.
