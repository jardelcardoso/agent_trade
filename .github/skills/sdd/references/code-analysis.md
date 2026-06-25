# Ferramentas de Análise de Código

Use degradação graciosa para busca de código e análise estrutural.

## Prioridade de Ferramentas

1. **ast-grep** (`sg`) - Busca estrutural baseada em padrões
2. **ripgrep** (`rg`) - Busca de texto rápida e sensível ao contexto
3. **grep** - Busca de texto padrão (sempre disponível)

## Detecção

Verifique a disponibilidade da ferramenta antes de usar:

```bash
# Verificar ast-grep
if command -v sg >/dev/null 2>&1; then
  # Usar ast-grep para busca estrutural
elif command -v rg >/dev/null 2>&1; then
  # Fallback para ripgrep
else
  # Usar grep padrão como fallback final
fi
```

## Exemplos de Uso

**Encontrando definições de função:**

```bash
# ast-grep (melhor - estrutural)
sg -p 'function $NAME($$$) { $$$ }'

# ripgrep (fallback - texto rápido)
rg '^function\s+\w+\(' --type-add 'source:*.[extension]' -t source

# grep (último recurso - básico)
grep -r '^function ' --include="*.[extension]"
```

**Encontrando imports/requires:**

```bash
# ast-grep
sg -p 'import { $$$ } from "$MODULE"'

# ripgrep
rg '^import .* from' --type-add 'source:*.[extension]' -t source

# grep
grep -r '^import ' --include="*.[extension]"
```

**Encontrando definições de classes/componentes:**

```bash
# ast-grep
sg -p 'class $NAME { $$$ }'

# ripgrep
rg '^(class|export class)\s+\w+' --type-add 'source:*.[extension]' -t source

# grep
grep -r '^class ' --include="*.[extension]"
```

## Escopo de Busca

**Melhores práticas:**

- Limitar a extensões de arquivos fonte relevantes para o projeto
- Excluir diretórios: `node_modules`, `vendor`, `dist`, `build`, `.git`
- Focar em diretórios fonte: `src`, `lib`, `app`
- Usar filtros de tipo de arquivo quando disponível

**Dicas de desempenho:**

- Usar padrões específicos em vez de buscas amplas
- Limitar a profundidade do diretório com `--max-depth` (ripgrep/grep)
- Cachear resultados para consultas repetidas

## Aviso de Fallback

Se o ast-grep não estiver disponível, exibir uma vez por sessão:

```
⚠️ ast-grep não detectado. Instale para análise de código estrutural mais precisa.
   https://ast-grep.github.io/guide/quick-start.html
```

## Quando Usar

- Encontrar padrões de uso em toda a base de código
- Identificar a estrutura e organização do código
- Localizar definições de funções/classes/componentes
- Analisar padrões de importação/dependência
- Análise de impacto de refatoração
- Navegação de código em bases de código desconhecidas
