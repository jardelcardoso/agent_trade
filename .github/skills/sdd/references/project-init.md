# Inicialização do Projeto

**Trigger:** "Inicializar projeto", "Configurar projeto", "Iniciar novo projeto"

## Processo

Extraia a visão do projeto através de Q&A iterativo (máx. 3-5 perguntas por mensagem):

**Perguntas essenciais:**

1. O que você está construindo?
2. Para quem é e qual problema resolve?
3. Qual stack tecnológica você está usando? (se souber)
4. O que está no escopo da v1? O que está explicitamente excluído?
5. Restrições críticas? (prazo, técnicas, recursos)

**Pare quando:** Houver uma compreensão clara da visão, objetivos e limites.

## Saída: .specs/project/PROJECT.md

**Estrutura:**

```markdown
# [Nome do Projeto]

**Visão:** [descrição de 1-2 sentenças]
**Para:** [usuários-alvo]
**Resolve:** [problema central sendo abordado]

## Objetivos

- [Objetivo primário com métrica de sucesso mensurável]
- [Objetivo secundário com métrica de sucesso mensurável]

## Tech Stack

**Core:**

- Framework: [nome + versão]
- Linguagem: [nome + versão]
- Banco de Dados: [nome]

**Dependências-chave:** [3-5 bibliotecas/frameworks críticos]

## Escopo

**v1 inclui:**

- [Capacidade principal 1]
- [Capacidade principal 2]
- [Capacidade principal 3]

**Explicitamente fora de escopo:**

- [O que NÃO está sendo construído]
- [O que NÃO está sendo construído]

## Restrições

- Prazo: [se aplicável]
- Técnicas: [se aplicável]
- Recursos: [se aplicável]
```

**Limite de tamanho:** 2.000 tokens (~1.200 palavras)

**Validação:**

- Visão clara em 1-2 sentenças?
- Objetivos possuem resultados mensuráveis?
- Limites de escopo estão explícitos?
