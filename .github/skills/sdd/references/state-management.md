# Gestão de Estado

**Objetivo:** Memória persistente entre sessões — decisões, bloqueadores, aprendizados.

## Estrutura

**Saída:** `.specs/project/STATE.md`

```markdown
# Estado

**Última Atualização:** [ISO timestamp]
**Trabalho Atual:** [Nome da Funcionalidade] - [Identificador da Tarefa]

---

## Decisões Recentes (Últimos 60 dias)

### AD-[NNN]: [Título da Decisão] ([data])

**Decisão:** [O que foi decidido]
**Motivo:** [Por que esta escolha]
**Compromisso (Trade-off):** [O que foi sacrificado]
**Impacto:** [Como isso afeta a implementação]

### AD-[NNN]: [Título da Decisão] ([data])

[Mesma estrutura]

---

## Bloqueadores Ativos

### B-[NNN]: [Descrição do Bloqueador]

**Descoberto em:** [Data]
**Impacto:** [Severidade e escopo]
**Contorno (Workaround):** [Solução temporária, se disponível]
**Resolução:** [Caminho para a correção permanente]

---

## Lições Aprendidas

### L-[NNN]: [Descrição do Aprendizado]

**Contexto:** [Situação ocorrida]
**Problema:** [O que deu errado]
**Solução:** [Como foi resolvido]
**Prevenção:** [O que este conhecimento evita no futuro]
```

## Quando Atualizar

| Evento                             | Ação                                      |
| ---------------------------------- | ----------------------------------------- |
| Escolha arquitetural significativa | Adicionar AD-[NNN]                        |
| Implementação bloqueada            | Adicionar B-[NNN]                         |
| Descoberta/aprendizado importante  | Adicionar L-[NNN]                         |
| Fim de sessão                      | Atualizar "Última Atualização" + "Trabalho Atual" |

## Gestão de Tamanho (Estratégia Híbrida)

**Zonas:**

- 🟢 <7k tokens: Nenhuma ação
- 🟡 7-10k tokens: Nota de rodapé "STATE.md em [X]k. Limpeza recomendada."
- 🔴 >10k tokens: Alerta ativo "STATE.md crítico ([X]k). Limpar agora?"

**Processo de Limpeza:**

- Mover decisões com mais de 60 dias para `STATE-ARCHIVE.md`
- Manter apenas bloqueadores ativos
- Preservar aprendizados recentes (<60 dias)

**Validação:**

- As decisões têm uma justificativa clara?
- Os bloqueadores incluem um caminho para a resolução?
- Os aprendizados são acionáveis?

---

## Preferências

Rastreie o estado de comportamento voltado ao usuário no `STATE.md`:

```markdown
## Preferências

**Orientações do Modelo Exibidas:** [Data ISO ou "nunca"]
```

**Atualizar quando:**

| Evento                            | Ação                          |
| --------------------------------- | ----------------------------- |
| Primeira dica do modelo fornecida | Definir data                 |
| Usuário reconhece/descarta        | Manter data (não repetir)     |
