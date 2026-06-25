# Implementação

**Objetivo**: Executar UMA tarefa por vez. Mudanças cirúrgicas. Marcar como concluída.

---

## OBRIGATÓRIO: Antes de Iniciar Qualquer Implementação

**Leia os [coding-principles.md](coding-principles.md) e declare:**

1. **Premissas** - O que estou assumindo? Alguma incerteza?
2. **Arquivos a alterar** - Liste APENAS os arquivos que esta tarefa requer
3. **Critérios de sucesso** - Como vou verificar se isso funciona?

⚠️ **Não prossiga sem declarar estes pontos explicitamente.**

---

## Processo

### 1. Escolher a Tarefa

O usuário especifica ("implementar T3") ou sugira a próxima disponível.

### 2. Verificar Dependências

Verifique o `tasks.md` - todas as dependências estão marcadas como concluídas?

❌ Se não: "T3 depende de T2, que não está pronta. Devo fazer a T2 primeiro?"

### 3. Declarar Plano de Implementação

Antes de escrever o código:

```
Arquivos: [lista]
Abordagem: [breve descrição]
Sucesso: [como verificar]
```

### 4. Implementar

- Siga o "O quê" (What) e "Onde" (Where) exatamente
- Referencie "Reutiliza" (Reuses) para padrões
- Aplique os [coding-principles.md](coding-principles.md):
  - O código mais simples que funciona
  - Altere APENAS os arquivos listados
  - Sem "scope creep" (aumento de escopo)

### 5. Verificar "Concluído Quando" (Done When)

Verifique todos os critérios antes de marcar como concluído.

### 6. Auto-verificação

Pergunte: "Um engenheiro sênior consideraria isso excessivamente complicado?"

- Sim → Simplifique antes de continuar
- Não → Marque a tarefa como concluída no `tasks.md`

---

## Template de Execução

```markdown
## Implementando T[X]: [Título da Tarefa]

**Leitura**: definição da tarefa no tasks.md
**Dependências**: [Todas concluídas? ✅ | Bloqueado por: TY]

### Pré-Implementação (OBRIGATÓRIO)

- **Premissas**: [declarar explicitamente]
- **Arquivos a alterar**: [listar APENAS estes]
- **Critérios de sucesso**: [como verificar]

### Implementação

[Realizar o trabalho]

### Verificação

- [x] Concluído quando critério 1
- [x] Concluído quando critério 2
- [x] Nenhuma mudança desnecessária feita
- [x] Corresponde aos padrões existentes

**Status**: ✅ Concluído | ❌ Bloqueado | ⚠️ Parcial
```

---

## Dicas

- **Uma tarefa por vez** - O foco previne erros
- **Ferramentas importam** - MCP errado = abordagem errada
- **Reutilizar economiza tokens** - Copie padrões, não reinvente a roda
- **Verificar antes de marcar como pronto** - Valide todos os critérios
- **Mantenha-se cirúrgico** - Altere apenas o necessário
