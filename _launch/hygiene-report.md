# Hygiene Report - zer0lint

**Mode:** AUDIT (published public repo - all proposed changes go to proposed-edits.md, not applied directly)

## README

| Check | Status | Notes |
|---|---|---|
| Hero visual | NEEDS-FIX | No image above H1. Spec requires centered 720px image before H1. |
| H1 | PASS | `# zer0lint` - correct |
| Tagline as `>` blockquote | NEEDS-FIX | First line is bold text `**AI memory extraction diagnostics.**`, not a `>` blockquote. |
| Badge row (5-7) | PARTIAL | 4 badges present (PyPI version, Python version, License, Hermes Labs). Missing: CI status, downloads. |
| 30-second pitch paragraph | PASS | "Is this you?" section + The Problem section cover this well. |
| Install (3 paths max) | PARTIAL | pip install present. Missing `uv tool install zer0lint` (standard for CLI tools). |
| Quick example (5-15 lines) | PASS | Multiple CLI examples shown. |
| "vs alternatives" section | NEEDS-FIX | No direct comparison table. "Ecosystem" section names cogito-ergo and zer0dex but doesn't compare to alternatives (manual spot-checking, other mem diagnostics). |
| Docs links | PARTIAL | GitHub links present. No CHANGELOG, CONTRIBUTING, CODE_OF_CONDUCT links (those files don't exist). |
| License line | NEEDS-FIX | "Apache 2.0" at bottom with no link to LICENSE file. Spec: `Apache 2.0 - see [LICENSE](LICENSE).` |
| Length (<= 300 lines) | PASS | 294 lines. Under limit. |
| TOC (required if >200 lines) | NEEDS-FIX | 294 lines and NO Table of Contents. Spec requires TOC if >200 lines. |
| Em-dashes | NEEDS-FIX | 19 em-dash occurrences in README (voice rule violation). Found in prose AND in code block CLI output - code blocks should be exempt. Prose em-dashes need replacing. |
| Banned footer pattern | PASS | Footer says "Built by Hermes Labs" - this is fine (not the "Built with ❤ by X" banned pattern). |
| Hermes Labs attribution | PASS | Present - badge + footer section. |

## Known README Bug (diagnosis)

**The cogito-ergo R@1 stat is stale.** README line 242 says:

```
Deploy retrieval  ->  cogito-ergo (two-stage retrieval, 85% R@1)
```

That 85% comes from a 31-case internal eval (2026-03-28). The actual LongMemEval benchmark (470 questions, 2026-04-15) shows:
- Baseline: 56.0% R@1
- Combined system (BM25 + turn chunking + nomic prefixes): 83.2% R@1
- Latest polish (2026-04-16): 89% R@1

The zer0lint README should cite either the verified 83.2% (reproducible, 470q) or omit the stat entirely since cogito-ergo is not yet publicly released with that benchmark. Citing 85% from a 31-case eval is misleading, though not deliberately so.

**Secondary finding:** The README also contains em-dashes in the prose (not just in code blocks). The pyproject.toml description itself has an em-dash: `"AI memory extraction diagnostics - works with mem0 or any HTTP memory endpoint."` - this should be a hyphen per voice rules, though pyproject.toml is code metadata, not a text artifact.

## llms.txt

| Check | Status | Notes |
|---|---|---|
| File exists | PASS | Present at repo root. |
| Who it's for | PASS | Clear audience description. |
| What it does | PASS | CLI reference included. |
| Canonical URLs | PASS | GitHub + PyPI URLs present. |
| Hermes Labs owner line | PASS | `https://hermes-labs.ai` present at bottom. |
| Format (no em-dashes) | PASS | No em-dashes in llms.txt. |

## CITATION.cff

| Check | Status | Notes |
|---|---|---|
| File exists | NOT-APPLICABLE | cli-tool classification does not require CITATION.cff. |

## LICENSE

| Check | Status | Notes |
|---|---|---|
| File exists | FAIL | No `LICENSE` file in repo root. pyproject.toml declares `license = {text = "Apache-2.0"}` but the actual file is absent. GitHub cannot detect license without the file. PyPI shows no license URL. |

## Badges

| Check | Status | Notes |
|---|---|---|
| PyPI version | PASS | `![PyPI version](https://img.shields.io/pypi/v/zer0lint)` |
| Python version | PASS | `![Python 3.9+](https://img.shields.io/pypi/pyversions/zer0lint)` |
| License | PASS | Present but uses hardcoded text not dynamic shield. |
| CI status | NEEDS-FIX | No `.github/workflows/` exists. No CI badge possible until CI is added. |
| Downloads | NEEDS-FIX | No downloads badge. |
| Hermes Labs | PASS | Custom badge present. |

## GitHub metadata

| Check | Status | Notes |
|---|---|---|
| Topics | NEEDS-FIX | Cogito memory (from 2026-03-28) says "Missing GitHub topics for zer0lint". `gh-metadata.sh` drafted with fix. |
| Description | UNKNOWN | Not checked without running `gh repo view`. |
| Homepage | NEEDS-FIX | Should point to hermes-labs.ai per Hermes Labs attribution rules. |

## Distribution files

| Check | Status | Notes |
|---|---|---|
| pyproject.toml | PASS | Present, complete with hatchling, scripts, optional-deps. |
| .github/workflows/test.yml | NEEDS-FIX | No CI at all. |
| .github/workflows/release.yml | NEEDS-FIX | No release automation. |
| CHANGELOG.md | NEEDS-FIX | Missing. |
| CONTRIBUTING.md | NEEDS-FIX | Missing. |
| CODE_OF_CONDUCT.md | NEEDS-FIX | Missing. |
| .pre-commit-config.yaml | NEEDS-FIX | Missing. ruff is configured in pyproject.toml but no pre-commit hook. |
| AGENTS.md vs agents.md | PASS (note) | File exists as `agents.md` (lowercase). Spec says AGENTS.md. Propose rename in proposed-edits.md. |

## Name check

`zer0lint` - intentional leetspeak. Consistent across PyPI, GitHub, CLI entry point. No rename proposed.
