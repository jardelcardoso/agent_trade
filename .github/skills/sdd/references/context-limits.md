# Limites de Contexto

## Limites de Tamanho de Arquivo

| Arquivo         | Tokens Máx. | ~Palavras | Aviso em      |
| --------------- | ----------- | --------- | ------------- |
| PROJECT.md      | 2.000       | 1.200     | 1.600 (80%)   |
| ROADMAP.md      | 3.000       | 1.800     | 2.400         |
| STATE.md        | 10.000      | 6.000     | 7.000 (70%)   |
| spec.md         | 5.000       | 3.000     | 4.000         |
| design.md       | 8.000       | 4.800     | 6.400         |
| tasks.md        | 10.000      | 6.000     | 8.000         |
| STACK.md        | 2.000       | 1.200     | 1.600         |
| ARCHITECTURE.md | 4.000       | 2.400     | 3.200         |
| CONVENTIONS.md  | 3.000       | 1.800     | 2.400         |
| STRUCTURE.md    | 2.000       | 1.200     | 1.600         |
| TESTING.md      | 4.000       | 2.400     | 3.200         |
| INTEGRATIONS.md | 5.000       | 3.000     | 4.000         |

## Zonas de Contexto

🟢 **Saudável** (<40k total): Silencioso
🟡 **Moderado** (40-60k): Nota de rodapé discreta
🔴 **Crítico** (>60k): Aviso ativo, sugerir otimização

## Monitoramento

Exiba o status do contexto no rodapé quando >40k:

```
📊 Contexto: 52k tokens (moderado)
  - STATE.md: 8k (zona amarela)
  - tasks.md: 11k (ok)
  - Total: 52k / 200k (26%)
```

## Princípios

**Alvo:** <40k tokens carregados (20% da janela)
**Reserva:** 160k+ tokens para trabalho, raciocínio e saídas
