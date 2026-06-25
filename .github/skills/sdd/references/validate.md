# Validar

**Objetivo**: Verificar se a implementação atende à especificação E aos princípios de codificação.

## Quando Validar

- Após completar uma história de usuário (todas as tarefas para P1, P2, etc.)
- Após completar todas as tarefas
- Quando o usuário solicitar validação

---

## Processo

### 1. Verificar Tarefas Concluídas

Percorra o `tasks.md`:

- [ ] Todas as tarefas marcadas como concluídas?
- [ ] Alguma bloqueada ou parcial?

### 2. Verificar Critérios de Aceite

Para cada história de usuário no `spec.md`:

```markdown
### P1: [Título da História]

**Critérios de Aceite**:

1. QUANDO [X] ENTÃO [Y] → [PASSOU/FALHOU]
2. QUANDO [X] ENTÃO [Y] → [PASSOU/FALHOU]
```

### 3. Verificar Casos de Borda

A partir dos casos de borda do `spec.md`:

- [ ] [Caso de borda 1] tratado corretamente
- [ ] [Caso de borda 2] tratado corretamente

### 4. Executar Testes (se aplicável)

```bash
# comando de teste do projeto
```

### 5. Verificação de Qualidade de Código (OBRIGATÓRIO)

Para cada arquivo alterado, verifique contra os [coding-principles.md](coding-principles.md):

| Verificação                                 | Passou? |
| ------------------------------------------  | ------- |
| Sem funcionalidades além do que foi pedido  |         |
| Sem abstrações para código de uso único     |         |
| Sem "flexibilidade" desnecessária adicionada|         |
| Alterou APENAS os arquivos necessários      |         |
| Não "melhorou" código não relacionado       |         |
| Corresponde aos padrões/estilo existentes   |         |
| Um engenheiro sênior aprovaria?             |         |

❌ Qualquer "Não"? → Corrija antes de marcar como completo.

### 6. Relatório

---

## Template de Relatório de Validação

```markdown
# Validação de [Funcionalidade]

**Data**: [AAAA-MM-DD]
**Especificação**: `.specs/features/[feature]/spec.md`

---

## Conclusão de Tarefas

| Tarefa | Status      | Notas   |
| ------ | ----------- | ------- |
| T1     | ✅ Concluído | -       |
| T2     | ✅ Concluído | -       |
| T3     | ⚠️ Parcial   | [Problema] |

---

## Validação de Histórias de Usuário

### P1: [Título da História] ⭐ MVP

| Critério       | Resultado |
| -------------- | --------- |
| QUANDO X ENTÃO Y| ✅ PASSOU |
| QUANDO A ENTÃO B| ✅ PASSOU |

**Status**: ✅ P1 Concluído

### P2: [Título da História]

| Critério       | Resultado |
| -------------- | --------- |
| QUANDO X ENTÃO Y| ✅ PASSOU |

**Status**: ✅ P2 Concluído
---

## Verificação de Princípios de Codificação

- [x] Simplicidade mantida (nada extra)
- [x] Padrões de design seguidos
- [x] Código testável e testado

## Veredito Final

**Status**: ✅ APROVADO | ❌ REJEITADO | ⚠️ APROVAÇÃO CONDICIONAL

**Notas**: [Comentários finais]
```
