# Classification - zer0lint

## Prior-art signal (Phase 0a - recorded BEFORE reading the repo)

### find_tool.py output

`python3 ~/ai-infra/find_tool.py "zer0lint"` returned 1 match:

- **name:** zer0lint
- **category:** infrastructure
- **one_liner:** "Tests whether facts you add() to a memory system survive extraction and come back on search()."
- **tags:** mem0, memory, extraction, diagnostics, ai-agent, linter, ingestion-test, custom_fact_extraction_prompt, ci-health-check, rich-cli
- **entry:** `cd ~/Documents/projects/zer0lint && PYTHONPATH=. python3 -m zer0lint check --config ~/.mem0/config.json`
- **installed:** false

`python3 ~/ai-infra/find_tool.py "mem0 diagnostics"` returned 3 matches with zer0lint as top result (relevance 0.6).

Signal: registry treats this as **infrastructure / diagnostics CLI**, not a library or framework.

### cogito recall output

`cogito recall "zer0lint"` returned 20 memories. Key facts:

1. "zer0lint is an ingestion health diagnostic for mem0-based agent memory"
2. "zer0lint published on PyPI and GitHub"
3. "zer0lint related to cogito-ergo and zer0dex"
4. "Missing GitHub topics for zer0lint as of 2026-03-28"
5. "No competitors for zer0lint, only manual spot-check guidance available for mem0"
6. "zer0lint ran against cogito_main corpus got 0/5 (CRITICAL) and fixed it to 5/5 (+100pp)"

Signal: memory confirms this is a diagnostics CLI, deployed against real production data with measured outcomes.

## Classification verdict

**Category: `cli-tool`**

Evidence from code:
- `pyproject.toml` declares `[project.scripts] zer0lint = "zer0lint.cli:app"` - this is the primary entrypoint
- `zer0lint/cli.py` uses Typer to define `check` and `generate` subcommands
- The tool has no importable Python API surface (no `__all__`, no exported classes/functions documented for library use)
- `zer0lint/__init__.py` exports only `__version__` (checked from structure)
- The manifest in `find_tool.py` shows `entry:` as a CLI command, not `from zer0lint import ...`

**Not `library`:** The Python package structure exists for packaging, but the intended UX is `zer0lint check` from a shell.
**Not `agent-framework`:** It diagnoses memory systems; it does not provide scaffolding for building agents.
**Not `research-artifact`:** Has real test data and a case study, but the primary artifact is the working CLI tool.

### Contradiction check

Prior-art signal: both find_tool.py and cogito agree this is an infrastructure CLI for mem0 diagnostics. My classification as `cli-tool` is consistent - no contradiction.

## Claim

See `claim.md`.

## Audience

AI engineers and agent developers who use mem0 (or any HTTP memory system) and have hit silent extraction failures where `add()` returns success but the agent can't recall facts.
