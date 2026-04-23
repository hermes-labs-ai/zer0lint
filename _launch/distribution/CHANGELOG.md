# Changelog

All notable changes to zer0lint are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
zer0lint uses [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

Planned for v0.3.0 based on the roadmap and open issues:

### Planned

- **CI health-check mode** - exit-code integration so `zer0lint check` can gate deploys
  (exits non-zero on CRITICAL/DEGRADED, useful in GitHub Actions, pre-deploy hooks)
- **JSON output flag** (`--output json`) - machine-readable score for pipeline integration
- **Custom fact set** - `zer0lint check --facts-file my_facts.json` for domain-specific test cases
  instead of the built-in 5 synthetic technical facts
- **zer0dex integration** - check dual-layer index health alongside extraction
- **Multi-backend batch check** - `zer0lint check --backends backends.json` to test multiple
  memory endpoints in one run, produce a comparison table

### Known issues

- HTTP mode `--http-wait` default of 1.5s may be too short for slow vector store backends
  (workaround: use `--http-wait 3.0`)

---

## [0.2.1] - 2026-04-13

### Added
- PyPI classifiers: Development Status, Intended Audience, License, Programming Language, Topic
- Author metadata: Hermes Labs, roli@hermes-labs.ai
- Project URLs: Homepage, Repository, Documentation, Issues
- Keywords for PyPI search: ai, agents, memory, mem0, extraction, diagnostics, llm, ollama, retrieval, vector-store

### Fixed
- `[project.urls]` section now includes all four canonical URLs

---

## [0.2.0] - 2026-04-13

### Added
- Universal HTTP mode: `zer0lint check --add-url <url> --search-url <url>` works with any
  memory system (cogito-ergo, Zep, LangMem, custom HTTP API) - no mem0 dependency required
- `--http-wait` flag: configurable wait time after `add()` before searching (default 1.5s)
- `--user-id` flag: override test user_id for isolation in HTTP mode
- `--save-prompt` flag: save generated extraction prompt to a file in HTTP mode
- Config-level injection: `zer0lint generate` writes to `custom_fact_extraction_prompt` in
  the mem0 config JSON (not passed at call time, which has no effect in mem0 v1.x)
- Validated flow: `generate` only applies the fix if it improves the score
- Timestamped backup before any config write
- Rich CLI output with color-coded status (HEALTHY/ACCEPTABLE/DEGRADED/CRITICAL)
- `--dry-run` flag: preview what `generate` would change without applying

### Changed
- Entry point renamed to `zer0lint` (was `zer0lint-cli` in v0.1)
- Replaced memory sampler with environment scanner for more robust test fact generation

### Breaking
- `zer0lint-cli` entrypoint removed; use `zer0lint` directly

---

## [0.1.0] - 2026-04-13

### Added
- Initial release: `zer0lint check` - injects 5 synthetic facts, measures round-trip recall
- `zer0lint generate` - 3-phase baseline + retest + apply
- mem0 config mode: reads standard `~/.mem0/config.json`
- Score thresholds: HEALTHY (>=80%), ACCEPTABLE (60-79%), DEGRADED (40-59%), CRITICAL (<40%)
- Case study result: mistral:7b default config 0/5 (0%), with zer0lint prompt 5/5 (100%)
- 0->100pp improvement on the real cogito_main corpus (2026-03-22)

---

[Unreleased]: https://github.com/hermes-labs-ai/zer0lint/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/hermes-labs-ai/zer0lint/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/hermes-labs-ai/zer0lint/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/hermes-labs-ai/zer0lint/releases/tag/v0.1.0
