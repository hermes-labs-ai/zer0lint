<div align="center">

<h1>zer0lint</h1>

zer0lint checks whether facts survive a memory system's add/search round trip. With a local mem0 config, it can compare a replacement extraction prompt and apply it after a clean improvement.

zer0lint is developed by [Hermes Labs](https://hermes-labs.ai).

Hermes Labs is an agentic infrastructure company building the reliability layer for autonomous systems.

[![CI](https://github.com/hermes-labs-ai/zer0lint/actions/workflows/ci.yml/badge.svg)](https://github.com/hermes-labs-ai/zer0lint/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/zer0lint.svg)](https://pypi.org/project/zer0lint/)
[![Python](https://img.shields.io/pypi/pyversions/zer0lint.svg)](https://pypi.org/project/zer0lint/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

</div>

`zer0lint` injects known facts and reports which ones come back. In mem0 config mode, it can compare your configured extraction prompt with a technical-fact prompt before changing the config. HTTP add/search mode measures fact survival but cannot isolate extraction or test a changed prompt.

- "mem0 says add worked, but the agent still forgets the important part."
- "Search returns something, but not the specific fact I stored."
- "We switched models and memory quality got worse for no obvious reason."
- "Our retrieval benchmark looks fine, but the batch behavior is still wrong."
- "I need to know whether facts survive before I tune extraction or retrieval."

```bash
# For mem0 config mode (includes the mem0 dependency)
pip install "zer0lint[mem0]"
```

```bash
zer0lint check --config ~/.mem0/config.json
```

```text
Score  : 0/5 (0%) — CRITICAL
For a mem0 config, run zer0lint generate to test a prompt change.
```

**When To Use It**

Use `zer0lint` when an add call succeeds but your agent later misses concrete facts. A low HTTP score tells you to investigate extraction and search separately; a low mem0 score gives you a prompt candidate to test.

**When Not To Use It**

Do not use `zer0lint` to pinpoint an HTTP pipeline stage, troubleshoot an API outage, or prove that one prompt fix generalizes to every memory pipeline.

## The Problem

The failure can be subtle. `add()` may return results while extraction drops the specific facts your agent needs; on some model and backend combinations it raises an error instead. Either way, the useful question is whether the fact survives a real add/search round trip.

zer0lint injects known facts and checks how many survive the round trip. The illustrative output below shows missing facts; inspect the underlying backend to learn whether extraction, indexing, or search lost them:

```
Score  : 0/5 — CRITICAL
  ⚠  Model upgrade: We switched from gpt-3.5-turbo to gpt-4o-mini...
  ⚠  API endpoint: The API service runs on port 8421 with TLS 1.3...
  ⚠  CI status: CI pipeline passed at commit a3f8c12...
  ⚠  Configuration: Auth tokens expire after 3600 seconds...
  ⚠  Version update: Updated Redis cluster to v7.2.4...
```

---

## Quick Start

```bash
# For mem0 config mode (includes the mem0 dependency)
pip install "zer0lint[mem0]"

# Step 1: diagnose
zer0lint check --config ~/.mem0/config.json

# Step 2: compare prompts without writing a config change
zer0lint generate --config ~/.mem0/config.json --dry-run

# Apply only if the comparison improves enough
zer0lint generate --config ~/.mem0/config.json
```

In mem0 config mode, your original config is backed up (timestamped) before any changes are written.

### HTTP add/search mode

Not using mem0? Use HTTP mode if your service accepts `POST` JSON with `text` and `user_id` at its add endpoint, and `text`, `limit`, and `user_id` at its search endpoint:

```bash
# Point at a server that implements the documented JSON contract
zer0lint check --add-url http://localhost:19420/add --search-url http://localhost:19420/recall_b

# A low score means facts did not survive this round trip. Inspect extraction and
# search in the backend separately; HTTP mode cannot test a changed prompt.
```

The exact request and response contract is below. Other products may need an adapter; their names alone do not establish compatibility.

---

## What It Does

### `zer0lint check`

Injects 5 synthetic technical facts into your selected backend, then measures round-trip recall. Uses your existing backend and credentials. A low score can reflect extraction, indexing, or search. Request errors produce `INCONCLUSIVE` and a nonzero exit code.

```
zer0lint v0.4.0 — fact-survival check
Config : ~/.mem0/config.json
Model  : mistral:7b
Prompt : default (mem0 built-in)

Error in new_retrieved_facts: Unterminated string starting at: line 1 column 10 (char 9)
Error in new_retrieved_facts: Expecting ',' delimiter: line 1 column 13 (char 12)

[CHECK] Using model: mistral:7b
[CHECK] Testing with 5 synthetic facts...
[CHECK] Score: 0/5 (0%) — CRITICAL
  ⚠  Model upgrade: We switched from gpt-3.5-turbo to gpt-4o-mini...
  ⚠  API endpoint: The API service runs on port 8421 with TLS 1.3...
  ⚠  CI status: CI pipeline passed on 2026-03-22 at commit a3f8c12...
  ⚠  Configuration: Auth tokens expire after 3600 seconds...
  ⚠  Version update: Updated Redis cluster to v7.2.4...

Score  : 0/5 (0%) — CRITICAL
If this is a mem0 config, run zer0lint generate to test a prompt change.
```

Statuses: **HEALTHY** (≥80%) · **ACCEPTABLE** (60–79%) · **DEGRADED** (40–59%) · **CRITICAL** (<40%)

### `zer0lint generate`

3-phase diagnostic + fix for **mem0 config mode**. Re-tests the prompt on your own config before applying it. If either phase has an add or search error, it reports `INCONCLUSIVE` and makes no config change, even if the re-test scored higher. A clean improvement must reach at least 4/5 facts (or all facts if you requested fewer than 4).

1. **Baseline** — test your current config as-is
2. **Re-test** — apply zer0lint's built-in technical-domain extraction prompt at config level
3. **Apply** — if the re-test scores higher, write the validated prompt to your config (with backup)

Example run shape (your numbers depend on your model and config):

```
[1/3] Baseline — testing current config as-is...
  Baseline score: <n>/5
    ❌ Configuration
    ❌ API endpoint
    ❌ CI status
    ❌ Model upgrade
    ❌ Version update

[2/3] Re-testing with zer0lint technical extraction prompt (config-level)...
  Improved score: <m>/5
    ✅ Configuration
    ✅ API endpoint
    ✅ CI status
    ✅ Model upgrade
    ✅ Version update

[3/3] Applying fix to config (only if the score improved)...
  ✅ Config updated.
  Backup at: ~/.mem0/config.backup.<timestamp>.json
```

---

## Where Extraction Actually Happens

A common mistake is trying to fix this by passing a custom prompt at call time:

```python
memory.add("...", prompt="extract technical facts")  # does nothing
```

**This has no effect in Mem0 when passed to `add()`.** Extraction instructions must live in the config. Current Mem0 uses `custom_instructions`; older supported Mem0 schemas used `custom_fact_extraction_prompt`. zer0lint detects the installed schema and writes the supported field. There is no error when an unsupported per-call prompt is ignored.

When both test phases complete without add/search errors and the new prompt improves enough, zer0lint writes it to the Mem0 config and backs up the original.

---

## Config Format

zer0lint reads a standard mem0 config JSON. Example:

```json
{
  "llm": {
    "provider": "ollama",
    "config": {
      "model": "mistral:7b",
      "ollama_base_url": "http://localhost:11434"
    }
  },
  "vector_store": {
    "provider": "chroma",
    "config": {
      "collection_name": "my_agent_memory",
      "path": "~/.mem0/chroma"
    }
  }
}
```

After `zer0lint generate`, it adds:

```json
{
  "custom_instructions": "You are a Technical Memory Organizer..."
}
```

On an older installed Mem0 schema, zer0lint preserves compatibility by writing the legacy `custom_fact_extraction_prompt` field instead.

For other backends, use the HTTP mode only when their endpoints meet the documented JSON contract. The Mem0 config fix does not apply to them.

---

## What zer0lint Checks

zer0lint injects synthetic technical facts into your memory instance, then measures how many survive the add/search round trip. It reports a score, a percentage, a status, and per-fact pass/fail. The result cannot identify a failing pipeline stage on its own.

Smaller models that struggle to emit well-formed structured JSON are the common failure case: the default extraction prompt can produce malformed output (`Unterminated string`, `Expecting ',' delimiter`) and silently drop facts. `zer0lint generate` proposes a stronger extraction prompt, re-runs the same check, and only writes the new prompt to config if the score improves — so any improvement is validated on your own model and config, not asserted.

---

## How It Works

zer0lint borrows the LLM you already have configured in your mem0 config. No new API keys, no new models, no cloud calls beyond what you already use.

In Mem0 config mode, it injects known facts, compares their survival under the current config and a technical-fact prompt, then writes that prompt only if the score improves enough. Your original config is backed up before the change. HTTP mode only runs the baseline check.

---

## Side Effects & Recovery

zer0lint writes to your real backend to run its check. Here's exactly what happens and how to undo it.

**What gets written**

- **mem0 mode:** synthetic test facts are added under a suffixed collection name (`<your_collection>_check`, `_baseline`, `_improved`) and a fresh per-run `user_id`, not your production namespace.
- **HTTP mode:** synthetic test facts are added under a per-run random `user_id` (e.g. `zer0lint_a1b2c3d4`) via your configured add endpoint. There is no collection suffixing — isolation depends entirely on your backend actually scoping by `user_id`.
- **Config writes:** `zer0lint generate` only writes to `--config` when the re-tested prompt scores higher than baseline, and always creates a timestamped backup first (`config.backup.<ISO timestamp>`).

**Cleanup — and how you know it happened**

After each phase, zer0lint attempts to delete the test facts it just wrote and returns a machine-readable receipt:

```json
{"mode": "delete", "user_id": "zer0lint_check", "attempted": 5, "deleted": 5, "failed": 0, "errors": []}
```

- `attempted` — test memories found for that isolated `user_id`
- `deleted` — how many were actually removed
- `failed` / `errors` — anything that didn't clean up, with the reason

`zer0lint check -v` and `zer0lint generate` print this receipt for every phase; `run_check()`/`run_generate()` also return it under `result["cleanup"]`, so you can assert on it in your own scripts instead of trusting a log line.

**HTTP mode does not delete.** The generic HTTP adapter only implements the documented add/search contract — it has no way to know your backend's delete endpoint. Isolation there relies entirely on the per-run random `user_id`; the receipt reports `"mode": "isolated_no_delete"` so this is explicit rather than a silent gap. If your backend doesn't scope reads by `user_id`, test facts persist — check your backend's data for the printed `user_id` if you need to remove them manually.

**Recovery**

- Config changes: restore from the printed `backup_path` (`cp <backup_path> <original_config_path>`).
- Leftover mem0 test data (`failed` > 0 in a receipt, or an interrupted run): delete the collection named in the receipt's context (`<collection>_check` / `_baseline` / `_improved`), or call `memory.delete_all(user_id=<receipt user_id>)` directly against your mem0 instance.
- Leftover HTTP-mode test data: search your backend for the `user_id` zer0lint printed and remove those entries through your backend's own tooling.

zer0lint never contacts a real memory store outside of the one you explicitly point it at with `--config`, `--add-url`, or `--search-url`.

---

## Installation

```bash
# HTTP mode (no extra dependencies)
pip install zer0lint

# mem0 config mode
pip install "zer0lint[mem0]"

# From source
git clone https://github.com/hermes-labs-ai/zer0lint
cd zer0lint
pip install -e .
```

**Requirements:** Python 3.9+. For mem0 config mode: `pip install zer0lint[mem0]`. For HTTP mode: no extra dependencies.

---

## Supported Systems

The HTTP adapter works with services that implement its JSON add/search request contract. It normalizes several response shapes (`results`, `hits`, `memories`, plain lists, and `text`/`content`/`memory` keys). It does not configure extraction or delete test facts.

| System | Mode | Notes |
|---|---|---|
| mem0 v1.x | `--config` flag | Config mode; covered by tests |
| HTTP memory API | `--add-url` + `--search-url` | Works if endpoints follow the add/search contract below |

The HTTP contract the adapter expects is documented in `zer0lint/http_adapter.py`.

---

## Limitations / What It Does Not Do

Grounded in what the code actually does:

- **It is not a semantic-correctness judge.** A fact counts as "recalled" when one of its keywords appears in the recall results (substring match, case-insensitive). It measures survival of identifiable content, not paraphrase quality or factual accuracy.
- **`generate` applies one built-in technical-domain prompt, not a per-domain generated prompt.** The fix it writes is a fixed prompt tuned for technical/agent-workspace facts. It is not adapted to your specific domain, and it is only written when the re-test scores higher than the baseline on your own model and config.
- **Synthetic test facts are technical/research-flavored.** `check` and `generate` inject facts from the `technical` and `research` sets. If your workload is medical, legal, or financial, the score reflects those technical facts, not your domain.
- **HTTP mode does not clean up after itself.** It isolates test data with a per-run random `user_id` rather than deleting it. If your backend ignores `user_id`, test facts may persist in the store. mem0 mode does delete its test facts after each phase and reports a pass/fail receipt — see [Side Effects & Recovery](#side-effects--recovery).
- **It does not pinpoint retrieval, extraction, embeddings, or vector-store failures.** It checks end-to-end fact survival. A passing score on these synthetic facts does not establish production recall quality.
- **One improving re-test does not imply generalization.** A higher score on the synthetic set is evidence the prompt helps your model on those facts — it is not a claim that it fixes every model, domain, or pipeline.

## Part of the Hermes Labs Reliability Stack

zer0lint is one of several open-source [Hermes Labs](https://github.com/hermes-labs-ai) tools for AI reliability. It can check a compatible memory backend's add/search path, or compare extraction prompts in a local mem0 config.

---

## License

Apache 2.0

---

## About Hermes Labs

Hermes Labs is an agentic infrastructure company building the reliability layer for autonomous systems.

Browse the [open-source catalog](https://hermes-labs.ai/open-source) or contact [roli@hermes-labs.ai](mailto:roli@hermes-labs.ai).
