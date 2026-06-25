# Criação do Roadmap

**Trigger:** "Criar roadmap", "Planejar funcionalidades", "Mapear fases do projeto"

## Processo

Com base no `PROJECT.md`, decomponha a visão em:

- Marcos (Milestones - incrementos entregáveis)
- Funcionalidades (capacidades voltadas ao usuário)
- Rastreamento de status (planejado/em progresso/concluído)

## Saída: .specs/project/ROADMAP.md

**Estrutura:**

```markdown
# Roadmap

**Marco Atual:** [nome do marco]
**Status:** Planejamento | Em Progresso | Concluído

---

## [Nome do Marco 1]

**Objetivo:** [O que torna este documento entregável]
**Alvo:** [Data ou critérios de conclusão]

### Funcionalidades

**[Nome da Funcionalidade]** - STATUS

- [Capacidade 1]
- [Capacidade 2]
- [Capacidade 3]

**[Nome da Funcionalidade]** - STATUS

- [Capacidade 1]
- [Capacidade 2]

---

## [Nome do Marco 2]

**Objetivo:** [O que este marco adiciona]

### Funcionalidades

**[Nome da Funcionalidade]** - PLANEJADO
**[Nome da Funcionalidade]** - PLANEJADO

---

## Considerações Futuras

- [Potencial capacidade futura]
- [Potencial capacidade futura]
```

**Valores de Status:**

- PLANEJADO: Não iniciado
- EM PROGRESSO: Em fase de implementação
- CONCLUÍDO: Entregue e verificado

**Limite de tamanho:** 3.000 tokens (~1.800 palavras)

**Estratégia de Atualização:**

- Mudar funcionalidades de PLANEJADO → EM PROGRESSO ao iniciar
- Mudar de EM PROGRESSO → CONCLUÍDO quando verificado
- Adicionar novos marcos conforme o projeto evolui

**Validação:**

- Cada marco tem um resultado entregável claro?
- As funcionalidades são capacidades voltadas ao usuário?
- O status reflete a realidade atual?
