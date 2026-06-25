---
name: sdd
description: Planejamento de projetos e funcionalidades com 4 fases - Especificar, Design, Tarefas, Implementar+Validar. Cria tarefas atômicas com critérios de verificação e mantém a memória persistente entre sessões. Independente de stack. Use quando: (1) Iniciar novos projetos (inicializar projeto, objetivos, roadmap), (2) Trabalhar com codebases existentes (mapear stack, arquitetura, convenções), (3) Planejar funcionalidades (requisitos, design, divisão de tarefas), (4) Implementar com verificação, (5) Rastrear decisões/bloqueadores entre sessões, (6) Pausar/retomar trabalho. Gatilhos em "inicializar projeto", "mapear codebase", "especificar funcionalidade", "design", "tarefas", "implementar", "pausar trabalho", "retomar trabalho".
---

# Spec-Driven Development (Desenvolvimento Baseado em Especificações)

Planeje e implemente projetos com precisão. Tarefas granulares. Dependências claras. Ferramentas certas.

```
│ ESPECIFICAR │ → │  DESIGN   │ → │  TAREFAS  │ → │ IMPLEMENTAR + VALIDAR  │
(O QUE construir)     (COMO construir)     (FAZER)           (CONSTRUIR + TESTAR)
```

## Estrutura do Projeto

```
.specs/
├── project/            # Gestão Global
│   ├── PROJECT.md      # Visão e Objetivos
│   ├── ROADMAP.md      # Funcionalidades e Marcos
│   └── STATE.md        # Memória entre sessões
├── codebase/           # Análise Brownfield (projetos existentes)
│   ├── STACK.md
│   ├── ARCHITECTURE.md
│   ├── CONVENTIONS.md
│   ├── STRUCTURE.md
│   ├── TESTING.md
│   └── INTEGRATIONS.md
└── features/           # Especificações de Funcionalidades
    └── [feature]/
        ├── spec.md
        ├── design.md
        └── tasks.md
```

## Fluxo de Trabalho

**Novo projeto:**

1. Inicializar projeto → `PROJECT.md`
2. Criar roadmap → `ROADMAP.md`
3. Especificar funcionalidades → fluxo existente

**Codebase existente:**

1. Mapear codebase → 6 documentos de brownfield
2. Inicializar projeto → `PROJECT.md` + `ROADMAP.md`
3. Especificar funcionalidades → fluxo existente

## Estratégia de Carregamento de Contexto

**Carga Base (~15k tokens):**

- `PROJECT.md` (se existir)
- `ROADMAP.md` (ao planejar/trabalhar em funcionalidades)
- `STATE.md` (memória persistente)

**Carga Sob Demanda:**

- Documentos de codebase (ao trabalhar em projeto existente)
- `spec.md` (ao trabalhar em funcionalidade específica)
- `design.md` (ao implementar a partir do design)
- `tasks.md` (ao executar tarefas)

**Nunca carregar simultaneamente:**

- Múltiplas especificações de funcionalidades
- Múltiplos documentos de arquitetura
- Documentos arquivados

**Alvo:** <40k tokens de contexto total
**Reserva:** 160k+ tokens para trabalho, raciocínio, saídas
**Monitoramento:** Exibir status quando >40k (veja [context-limits.md](references/context-limits.md))

## Comandos

**Nível de Projeto:**
| Padrão de Gatilho | Referência |
|-------------------|------------|
| Inicializar projeto, configurar projeto | [project-init.md](references/project-init.md) |
| Criar roadmap, planejar funcionalidades | [roadmap.md](references/roadmap.md) |
| Mapear codebase, analisar código existente | [mapping-codebase.md](references/mapping-codebase.md) |
| Registrar decisão, registrar bloqueador | [state-management.md](references/state-management.md) |
| Pausar trabalho, encerrar sessão | [session-handoff.md](references/session-handoff.md) |
| Retomar trabalho, continuar | [session-handoff.md](references/session-handoff.md) |

**Nível de Funcionalidade:**
| Padrão de Gatilho | Referência |
|-------------------|------------|
| Especificar funcionalidade, definir requisitos (O QUE construir )  | [specify.md](references/specify.md) |
| Design da funcionalidade, arquitetura (COMO construir) | [design.md](references/design.md) |
| Dividir em tarefas, criar tarefas | [tasks.md](references/tasks.md) |
| Implementar tarefa, construir | [implement.md](references/implement.md) |
| Validar, verificar, testar | [validate.md](references/validate.md) |

**Ferramentas e Princípios:**
| Padrão de Gatilho | Referência |
|-------------------|------------|
| Princípios de codificação | [coding-principles.md](references/coding-principles.md) |
| Análise de código | [code-analysis.md](references/code-analysis.md) |
| Limites de contexto | [context-limits.md](references/context-limits.md) |
