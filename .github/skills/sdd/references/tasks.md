# Fase 3: Tarefas

**Objetivo**: Divisão em tarefas GRANULARES e ATÔMICAS. Dependências claras. Ferramentas certas. Plano de execução paralela.

## Por que Tarefas Granulares?

| Tarefa Vaga (RUIM) | Tarefas Granulares (BOA)             |
| ------------------ | ------------------------------------ |
| "Criar formulário" | T1: Criar componente de input de e-mail |
|                    | T2: Adicionar função de validação de e-mail |
|                    | T3: Criar botão de envio             |
|                    | T4: Adicionar gestão de estado do formulário |
|                    | T5: Conectar formulário à API        |
| "Implementar auth" | T1: Criar formulário de login        |
|                    | T2: Criar formulário de cadastro     |
|                    | T3: Adicionar utilitário de armazenamento de token |
|                    | T4: Criar serviço de API de autenticação |
|                    | T5: Adicionar proteção de rotas      |

**Benefícios da granularidade:**

- **Agentes não erram** — Foco único, sem ambiguidade.
- **Fácil de testar** — Cada tarefa = um resultado verificável.
- **Paralelizável** — Tarefas independentes rodam simultaneamente.
- **Erros isolados** — Uma falha não bloqueia tudo.

**Regra**: Uma tarefa = APENAS UM destes:

- Um componente
- Uma função
- Um endpoint de API
- Uma alteração de arquivo

---

## Processo

### 1. Revisar o Design

Leia o `.specs/[feature]/design.md` antes de criar as tarefas.

### 2. Dividir em Tarefas Atômicas

**Tarefa = UM entregável**. Exemplos:

- ✅ "Criar interface UserService" (um arquivo, um conceito)
- ❌ "Implementar gestão de usuários" (muito vago, múltiplos arquivos)

### 3. Definir Dependências

O que DEVE ser feito antes que esta tarefa possa começar?

### 4. Criar Plano de Execução

Agrupe tarefas em fases. Identifique o que pode rodar em paralelo.

### 5. PERGUNTAR sobre MCPs e Skills

**CRÍTICO**: Antes da execução, pergunte ao usuário:

> "Para cada tarefa, quais ferramentas devo usar?"
>
> **MCPs Disponíveis**: [lista do projeto ou usuário]
> **Skills Disponíveis**: [lista do projeto ou usuário]

---

## Template: `.specs/[feature]/tasks.md`

```markdown
# Tarefas de [Funcionalidade]

**Design**: `.specs/[feature]/design.md`
**Status**: Rascunho | Aprovado | Em Progresso | Concluído

---

## Plano de Execução

### Fase 1: Fundação (Sequencial)

Tarefas que devem ser feitas primeiro, em ordem.

```
T1 → T2 → T3
```

### Fase 2: Implementação Principal (Paralelo OK)

Após a fundação, estas podem rodar em paralelo.

```
     ┌→ T4 ─┐
T3 ──┼→ T5 ─┼──→ T8
     └→ T6 ─┘
T7 ──────→
```

---

## Detalhamento das Tarefas

### [ID da Tarefa]: [Título Curto e Acionável]

- **O quê (What)**: [Descrição precisa do que construir]
- **Onde (Where)**: `src/path/to/file`
- **Reutiliza (Reuses)**: [Referência ao design/reutilização]
- **Ferramentas (Tools)**: [MCPs ou Skills sugeridos]
- **Depende de (Depends on)**: [IDs de outras tarefas]
- **Concluído Quando (Done When)**: [Critério de verificação testável]
- **Custo Estimado**: [Baixo | Médio | Alto]

---

## Rastreamento de Status

- [ ] T1: [Título]
- [ ] T2: [Título]
- [ ] T3: [Título]
```
