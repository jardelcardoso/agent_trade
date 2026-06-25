# Mapeamento Brownfield

**Trigger:** "Map codebase", "Analyze existing code", "Document current architecture"

**Objetivo:** Compreender a estrutura do projeto existente antes de adicionar novas funcionalidades.

## Processo

**Abordagem de alto nível:**

1. Explorar a estrutura de diretórios sistematicamente
2. Identificar a stack tecnológica a partir dos manifestos de dependência
3. Extrair padrões de amostras representativas de código
4. Documentar convenções e arquiteturas observadas
5. Catalogar integrações externas

**Profundidade da análise:**

- Amostrar 5-10 arquivos representativos por categoria
- Focar em consistência e padrões, não em cobertura exaustiva
- Extrair exemplos reais, não suposições

## Saída: 6 Arquivos em .specs/codebase/

---

### 1. STACK.md

**Propósito:** Documentar a stack tecnológica e dependências.

**Limite de tamanho:** 2.000 tokens (~1.200 palavras)

**Extrair de:**

- Arquivos de manifesto de dependência
- Configuração de build
- Configuração de runtime

**Documentar:**

```markdown
# Tech Stack

**Analisado em:** [data]

## Core

- Framework: [nome detectado + versão]
- Linguagem: [nome detectado + versão]
- Runtime: [nome detectado + versão]
- Gerenciador de pacotes: [gerenciador detectado]

## Frontend (se aplicável)

- Framework de UI: [nome + versão]
- Estilização: [abordagem + ferramentas]
- Gerenciamento de Estado: [biblioteca/padrão]
- Manipulação de Formulários: [biblioteca, se presente]

## Backend (se aplicável)

- Estilo de API: [REST/GraphQL/gRPC + framework]
- Banco de Dados: [ORM/query builder + sistema de banco de dados]
- Autenticação: [biblioteca/abordagem]

## Testes

- Unitários: [framework]
- Integração: [framework]
- E2E: [framework, se presente]

## Serviços Externos

- [Categoria]: [Nome do serviço]
- [Categoria]: [Nome do serviço]

## Ferramentas de Desenvolvimento

- [Categoria da ferramenta]: [Nome da ferramenta]
```

**Instruções:**

- Extrair de arquivos de dependência reais
- Incluir versões para as principais dependências
- Categorize por propósito
- Anotar explicitamente os frameworks de teste

---

### 2. ARCHITECTURE.md

**Propósito:** Documentar padrões arquiteturais e fluxo de dados.

**Limite de tamanho:** 4.000 tokens (~2.400 palavras)

**Extrair de:**

- Organização de diretórios
- Análise da estrutura do código
- Padrões repetidos entre os arquivos

**Documentar:**

```markdown
# Arquitetura

**Padrão:** [Padrão identificado - monólito/microserviços/modular/etc]

## Estrutura de Alto Nível

[Criar diagrama/descrição baseado na organização real]

## Padrões Identificados

### [Nome do Padrão]

**Localização:** [onde este padrão reside]
**Propósito:** [o que ele alcança]
**Implementação:** [como está estruturado]
**Exemplo:** [referência ao arquivo/função real]

### [Nome do Padrão]

[Mesma estrutura]

## Fluxo de Dados

### [Fluxo Chave - ex: Autenticação/Pagamento/etc]

[Mapear o fluxo real a partir da análise do código]

### [Fluxo Chave]

[Mapear fluxo real]

## Organização do Código

**Abordagem:** [baseada em funcionalidades/baseada em camadas/domain-driven/etc]

**Estrutura:**
[Documentar a organização real dos diretórios]

**Limites de Módulos:**
[Como o código é dividido em módulos/pacotes]
```

**Instruções:**

- Identificar padrões a partir do código real, não de suposições
- Documentar decisões arquiteturais observadas
- Criar diagramas de fluxo para caminhos críticos
- Referenciar exemplos concretos da base de código

---

### 3. CONVENTIONS.md

**Propósito:** Documentar estilo de código e convenções de nomenclatura.

**Limite de tamanho:** 3.000 tokens (~1.800 palavras)

**Extrair de:**

- Analisar 5-10 arquivos representativos
- Identificar padrões consistentes
- Observar as convenções reais em uso

**Documentar:**

```markdown
# Convenções de Código

## Convenções de Nomenclatura

**Arquivos:**
[Padrão observado - documentar a abordagem real]
Exemplos: [nomes de arquivos reais da base de código]

**Funções/Métodos:**
[Padrão observado]
Exemplos: [nomes de funções reais]

**Variáveis:**
[Padrão observado]
Exemplos: [nomes de variáveis reais]

**Constantes:**
[Padrão observado]
Exemplos: [nomes de constantes reais]

## Organização do Código

**Declaração de Importação/Dependência:**
[Padrão de ordenação observado]
[Exemplo de um arquivo real]

**Estrutura de Arquivo:**
[Organização observada dentro dos arquivos]
[Exemplo de um arquivo real]

## Segurança de Tipos/Documentação

**Abordagem:** [Sistema de tipos/abordagem de documentação utilizada]
[Exemplo do código real]

## Tratamento de Erros

**Padrão:** [Abordagem de tratamento de erros observada]
[Exemplo do código real]

## Comentários/Documentação

**Estilo:** [Quando/como os comentários são usados]
[Exemplo do código real]
```

**Instruções:**

- Extrair padrões de amostras de código reais
- Documentar as convenções observadas, não as convenções ideais
- Incluir exemplos concretos da base de código
- Observar exceções ou variações onde houver

---

### 4. STRUCTURE.md

**Propósito:** Documentar o layout do diretório e a organização dos arquivos.

**Limite de tamanho:** 2.000 tokens (~1.200 palavras)

**Documentar:**

```markdown
# Estrutura do Projeto

**Root:** [caminho da raiz do projeto]

## Árvore de Diretórios

[Representação visual da árvore - no máximo 3 níveis de profundidade]

## Organização dos Módulos

### [Nome do Módulo/Área]

**Propósito:** [o que esta área trata]
**Localização:** [onde os arquivos residem]
**Arquivos principais:** [arquivos importantes nesta área]

### [Nome do Módulo/Área]

[Mesma estrutura]

## Onde as Coisas Residem

**[Funcionalidade/Recurso]:**

- UI/Interface: [localização]
- Lógica de Negócio: [localização]
- Acesso a Dados: [localização]
- Configuração: [localização]

**[Funcionalidade/Recurso]:**
[Mesma estrutura]

## Diretórios Especiais

**[Nome do diretório]:**
**Propósito:** [o que pertence aqui]
**Exemplos:** [arquivos principais neste diretório]
```

**Instruções:**

- Criar visualização em árvore da estrutura real de diretórios
- Limitar a profundidade para manter a legibilidade
- Documentar o propósito dos principais diretórios
- Mapear funcionalidades para localizações físicas

---

### 5. TESTING.md

**Propósito:** Documentar a infraestrutura e os padrões de teste.

**Limite de tamanho:** 4.000 tokens (~2.400 palavras)

**Documentar:**

```markdown
# Infraestrutura de Testes

## Frameworks de Teste

**Unitários/Integração:** [nome do framework + versão]
**E2E:** [nome do framework + versão]
**Cobertura:** [ferramenta, se usada]

## Organização dos Testes

**Localização:** [onde os testes residem]
**Nomenclatura:** [padrão de nomenclatura de arquivos de teste]
**Estrutura:** [como os testes são organizados]

## Padrões de Teste

### Testes Unitários

**Abordagem:** [padrão observado]
**Localização:** [onde os testes unitários residem]
[Descrição do padrão real utilizado]

### Testes de Integração

**Abordagem:** [padrão observado]
**Localização:** [onde os testes de integração residem]
[Descrição do padrão real utilizado]

### Testes E2E

**Abordagem:** [padrão observado, se presente]
**Localização:** [onde os testes E2E residem]
[Descrição do padrão real utilizado]

## Execução de Testes

**Comandos:** [como executar os testes]
**Configuração:** [abordagem de configuração de teste]

## Metas de Cobertura

**Atual:** [se mensurável]
**Metas:** [se documentado]
**Aplicação:** [se automatizada]
```

**Instruções:**

- Identificar frameworks de teste a partir de dependências e código
- Documentar os padrões de teste reais observados
- Observar a abordagem de organização de testes
- Incluir instruções de execução

---

### 6. INTEGRATIONS.md

**Propósito:** Documentar integrações de serviços externos.

**Limite de tamanho:** 5.000 tokens (~3.000 palavras)

**Documentar:**

```markdown
# Integrações Externas

## [Categoria de Serviço]

**Serviço:** [nome do serviço]
**Propósito:** [o que esta integração fornece]
**Implementação:** [onde a integração reside no código]
**Configuração:** [como o serviço é configurado]
**Autenticação:** [abordagem de autenticação, se aplicável]

## [Categoria de Serviço]

[Mesma estrutura]

## Integrações de API

### [Nome da API]

**Propósito:** [o que esta API fornece]
**Localização:** [onde reside o cliente/código da API]
**Autenticação:** [método de autenticação]
**Endpoints principais:** [principais endpoints usados]

## Webhooks

### [Fonte do Webhook]

**Propósito:** [quais eventos são tratados]
**Localização:** [localização do handler de webhook]
**Eventos:** [event types processados]

## Jobs de Segundo Plano

**Sistema de fila:** [sistema, se usado]
**Localização:** [onde as definições de job residem]
**Jobs:** [principais jobs de segundo plano]
```

**Instruções:**

- Identificar integrações a partir do código e da configuração
- Documentar abordagens de autenticação
- Anotar handlers de webhooks, se presentes
- Incluir infraestrutura de jobs de segundo plano

---

## Orçamento Total de Contexto

**Combinado:** ~14.000 tokens (7% da janela de contexto)
**Aceitável para:** Projetos Brownfield que requerem compreensão da base de código
**Estratégia de carregamento:** Carregar docs relevantes sob demanda baseada na tarefa
