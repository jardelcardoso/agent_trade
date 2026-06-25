# Handoff de Sessão

## Pausar Trabalho

**Trigger:** "Pausar trabalho", "Encerrar sessão", "Criar handoff"

**Objetivo:** Criar um ponto de controle do estado atual para retomada futura.

**Saída:** `.specs/HANDOFF.md` (sobrescreve o anterior)

**Alvo de tamanho:** ~500 tokens

**Estrutura:**

```markdown
# Handoff

**Data:** [ISO timestamp]
**Funcionalidade:** [nome da funcionalidade]
**Tarefa:** [identificador da tarefa] - [breve status]

## Concluído ✓

- [Item de trabalho concluído]
- [Item de trabalho concluído]

## Em Progresso

- [Trabalho atual] ([porcentagem ou status])
- Localização específica: [arquivo:linha, se aplicável]

## Pendente

- [Próximo passo imediato]
- [Passo seguinte]

## Bloqueadores

- [Descrição do bloqueador] - [impacto]

## Contexto

- Branch: [git branch, se aplicável]
- Não commitado: [arquivos com alterações]
- Decisões relacionadas: [referências ao STATE.md, se aplicável]
```

**Instruções:**

- Concentre-se em informações acionáveis para a retomada.
- Inclua referências específicas de arquivos/linhas onde for relevante.
- Anote explicitamente as alterações não commitadas.
- Referencie entradas relacionadas no `STATE.md`, se aplicável.

## Retomar Trabalho

**Gatilho:** "Retomar trabalho", "Continuar", "Carregar handoff"

**Processo:**

1. Carregar `HANDOFF.md`
2. Carregar `STATE.md` para contexto
3. Resumir a posição atual
4. Propor a próxima ação

**Padrão de resposta:**

- "Retomando [funcionalidade] na [tarefa]"
- "Concluído: [resumo]"
- "A seguir: [ação imediata]"
- "Continuar com [passo específico]?"
