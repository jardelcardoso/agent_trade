# Fase 1: Especificar

**Objetivo**: Capturar O QUE construir com requisitos testáveis.

## Processo

### 1. Esclarecer Requisitos

Pergunte ao usuário (2-3 perguntas para começar):

- "Que problema você está resolvendo?"
- "Quem é o usuário e qual é a sua dor?"
- "Como é o sucesso deste projeto?"

Se necessário:

- "Quais são as restrições (tempo, tecnologia, recursos)?"
- "O que está explicitamente fora de escopo?"

### 2. Capturar Histórias de Usuário com Prioridades

**P1 = MVP** (deve ser entregue), **P2** (deveria ter), **P3** (desejável)

Cada história DEVE ser **testável de forma independente** - você deve conseguir implementar e demonstrar apenas essa história.

### 3. Escrever Critérios de Aceite

Use o formato **QUANDO/ENTÃO/DEVE** - é preciso e testável:

- QUANDO [evento/ação] ENTÃO [sistema] DEVE [resposta/comportamento]

---

## Template: `.specs/[feature]/spec.md`

```markdown
# Especificação de [Nome da Funcionalidade]

## Declaração do Problema

[Descreva o problema em 2-3 sentenças. Qual dor estamos resolvendo? Por que agora?]

## Objetivos

- [ ] [Objetivo primário com resultado mensurável]
- [ ] [Objetivo secundário com resultado mensurável]

## Fora de Escopo

- [Explicitamente NÃO construir: X]
- [Explicitamente NÃO construir: Y]

---

## Histórias de Usuário

### P1: [Título da História] ⭐ MVP

**História de Usuário**: Como [papel], eu quero [capacidade] para que [benefício].

**Por que P1**: [Por que isso é crítico para o MVP]

**Critérios de Aceite**:

1. QUANDO [ação/evento do usuário] ENTÃO o sistema DEVE [comportamento esperado]
2. QUANDO [ação/evento do usuário] ENTÃO o sistema DEVE [comportamento esperado]
3. QUANDO [caso de borda] ENTÃO o sistema DEVE [tratamento adequado]

**Teste Independente**: [Como verificar que esta história funciona sozinha - ex: "Pode demonstrar fazendo X e vendo Y"]

---

### P2: [Título da História]

**História de Usuário**: Como [papel], eu quero [capacidade] para que [benefício].

**Por que P2**: [Por que isso não é MVP, mas é importante]

**Critérios de Aceite**:

1. QUANDO [evento] ENTÃO o sistema DEVE [comportamento]
2. QUANDO [evento] ENTÃO o sistema DEVE [comportamento]

**Teste Independente**: [Como verificar]

---

### P3: [Título da História]

**História de Usuário**: Como [papel], eu quero [capacidade] para que [benefício].

**Por que P3**: [Por que isso é um "desejável"]

**Critérios de Aceite**:

1. QUANDO [evento] ENTÃO o sistema DEVE [comportamento]

---

## Casos de Borda

### [Caso de Borda 1]
QUANDO [condição incomum] ENTÃO o sistema DEVE [resposta de segurança/sucesso]

---

## Restrições de Design (Opcional)

- [Restrição 1]
- [Restrição 2]
```
