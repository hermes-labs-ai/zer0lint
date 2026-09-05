# Changelog

## 0.3.0

Problem: `check` and `generate` wrote synthetic test facts into a real mem0
store to measure extraction survival, but never removed them and gave no
signal about what was left behind — every run silently accumulated test data
with no receipt to audit or clean up against.

- `check` and `generate` now delete the test facts they write in mem0 mode
  after each phase and return a machine-readable cleanup receipt
  (`attempted`/`deleted`/`failed`/`errors`) instead of leaving test data
  behind with no record of what happened. Printed on `check -v` and
  `generate`, and returned under `result["cleanup"]` for scripting.
- HTTP mode still cannot delete (the generic add/search contract has no
  delete endpoint) — the receipt now reports this explicitly as
  `"mode": "isolated_no_delete"` rather than silently doing nothing, and
  isolation still depends entirely on the backend scoping reads by the
  per-run random `user_id`.
- Added a regression test against the actually-installed Mem0 `MemoryConfig`
  (not just fakes) to catch upstream schema drift immediately.
- Added a generic, disposable local HTTP fixture (`tests/http_fixture.py`)
  and adapter tests (`tests/test_http_adapter.py`) that exercise HTTP mode
  end-to-end without contacting a real memory store.
- Documented exact write/cleanup side effects and recovery steps in the
  README under "Side Effects & Recovery."

## 0.2.4

- Use Mem0's current `custom_instructions` field while retaining compatibility
  with older schemas that require `custom_fact_extraction_prompt`.
- Preserve the configured extraction prompt during baseline diagnostics and
  replace it only when an explicit override is tested or applied.
- Add regression coverage for current and legacy Mem0 configuration behavior.

## 0.2.3

- Add HTTP response-shape compatibility for common add/search memory APIs.
- Isolate HTTP diagnostic runs by user ID, including separate baseline and improved phases for `generate`.
- Add tests for HTTP isolation and a CI workflow across Python 3.9–3.13.
- Clarify first use, HTTP-mode limits, and the distinction between extraction diagnostics and retrieval health.
- Add release guards that require a matching `v<version>` tag, matching package metadata, expected artifacts, and a clean wheel install before PyPI publishing.

## 0.2.1

- Release universal HTTP mode.
