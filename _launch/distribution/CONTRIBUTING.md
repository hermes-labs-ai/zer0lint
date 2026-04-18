# Contributing to zer0lint

## Setup

```bash
git clone https://github.com/roli-lpci/zer0lint
cd zer0lint
pip install -e ".[dev]"
```

## Running tests

```bash
pytest tests/ -v
```

All tests must pass before submitting a PR.

## Linting

```bash
ruff check zer0lint/
ruff format zer0lint/
```

ruff is configured in `pyproject.toml`. Line length: 100. Target: Python 3.9+.

## Project structure

```
zer0lint/
  cli.py          - Typer CLI: check + generate subcommands
  orchestrator.py - Main workflow logic (run_check, run_generate)
  tester.py       - Synthetic fact injection and round-trip recall
  http_adapter.py - Universal HTTP mode (any memory endpoint)
  analyzer.py     - Score calculation and status classification
  fixer.py        - Config writing with backup
  sampler.py      - Synthetic fact generation
  scanner.py      - Environment scanning for config detection
tests/
  test_fixer.py
  test_sampler.py
  test_tester.py
```

## Submitting a PR

1. Fork the repo and create a feature branch off `main`
2. Add tests for any new behavior
3. Run `ruff check` and `pytest` - both must pass
4. Open a PR against `main` with a short description of the change

## Reporting bugs

Open an issue at https://github.com/roli-lpci/zer0lint/issues. Include:
- zer0lint version (`zer0lint --version`)
- Python version
- Operating system
- The exact command you ran
- Expected vs actual output
