% Projeto Template — Instruções para agentes (Clean Code em Python)

## Visão Geral

Este documento orienta agentes/assistentes e desenvolvedores para trabalhar em projetos Python com foco em Clean Code, legibilidade, testes e qualidade. Substitua marcadores como CriptoContext conforme necessário.

## Estrutura Recomendada (Python)

- `src/` — código-fonte do pacote/ módulo principal
  - `config/` — configuração e gerenciamento de ambiente
  - `models/` — objetos de domínio, DTOs, dataclasses
  - `usecases/` — regras de negócio e casos de uso
  - `adapters/` — implementações concretas (bancos, APIs, etc)
  - `worker.py` ou `main.py` — ponto de entrada para execução
- `tests/` — testes automatizados (pytest)
- `docs/` — documentação do projeto
- `scripts/` — utilitários e scripts de manutenção
- `scripts/ci/` — scripts/definições usadas pela CI
- `pyproject.toml` — configuração de build e ferramentas (recomendado)
- `requirements.txt` ou `poetry.lock` — dependências (conforme gerenciador escolhido)
- `README.md`, `CHANGELOG.md`, `LICENSE`

## Padrões e Convenções (Python Clean Code)

- **PEP 8 / PEP 257 / PEP 8 naming**: siga PEP 8 para estilo e convenções; escreva docstrings conforme PEP 257.
- **Tipagem**: prefira type hints (PEP 484) e use `mypy` para checagem estática quando possível.
- **Funções pequenas**: mantenha funções com responsabilidade única e tamanho reduzido.
- **Nomes descritivos**: variáveis, funções e classes com nomes claros e intencionais.
- **Imutabilidade quando aplicável**: prefira estruturas imutáveis e evite efeitos colaterais.
- **Exceptions claras**: lance exceções específicas e documente contratos.

## Ferramentas recomendadas

- **Formatação**: `black` (formato consistente)
- **Ordenação de imports**: `isort`
- **Lint/fast checker**: `ruff` ou `flake8` (ruff pode substituir isort/black/flake8 em muitos casos)
- **Type checker**: `mypy` (opcional, recomendado para projetos médios/grandes)
- **Testes**: `pytest`
- **Pre-commit hooks**: `pre-commit` com hooks para black/isort/ruff/mypy/pytest

## Gerenciamento de dependências e ambientes

- Use ambientes virtuais (`venv`) ou ferramentas como `poetry`/`pipenv`.
- Para projetos modernos, prefira `pyproject.toml` como fonte única de configuração.
- Exemplo com `venv` + pip:

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Ou com `poetry`:

```bash
poetry install
poetry shell
```

## Executar / Testar (comandos úteis)

- Instalar dependências (pip):

```bash
pip install -r requirements.txt
```

- Rodar testes com `pytest`:

```bash
pytest -q
```

- Rodar `black` e `isort`:

```bash
black src tests
isort src tests
```

- Checar tipos (mypy):

```bash
mypy src
```

## CI / Pipeline

- Configure a pipeline para rodar: formatação/lint, checagem de tipos, testes e análise de cobertura.
- Integre `pre-commit` para bloquear pushes com código mal formatado ou com erros básicos.

## Boas práticas para agentes e desenvolvedores

- Planeje pequenas mudanças e abra PRs atômicos com mensagens claras.
- Inclua testes para novos comportamentos e correções de bugs.
- Priorize legibilidade sobre micro-otimizações prematuras.
- Documente decisões arquiteturais importantes em `docs/` ou `.specs/`.

## Pre-commit e hooks recomendados

- Exemplo mínimo de `.pre-commit-config.yaml`:

```yaml
repos:
	- repo: https://github.com/psf/black
		rev: stable
		hooks:
			- id: black
	- repo: https://github.com/PyCQA/isort
		rev: stable
		hooks:
			- id: isort
	- repo: https://github.com/charliermarsh/ruff
		rev: stable
		hooks:
			- id: ruff
```

## Executar / Testar (exemplos atualizados)

- Instalar (venv):

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

- Rodar teste unitário:

```bash
pytest tests
```

## Checklist inicial (sugestão)

- [ ] Adicionar `pyproject.toml` com `tool.black`/`tool.isort` configurações
- [ ] Configurar `pre-commit` e instalar hooks
- [x] Adicionar `pytest` com cobertura mínima
- [ ] Definir `mypy` (se usar) e configurar CI

## Referências úteis

- PEP 8: https://peps.python.org/pep-0008/
- PEP 257 (docstrings): https://peps.python.org/pep-0257/
- Black: https://github.com/psf/black
- Pytest: https://docs.pytest.org/

---
Adapte estas recomendações conforme o porte do projeto e as preferências do time.
