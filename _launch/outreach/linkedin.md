# LinkedIn draft

---

We found a silent failure mode in mem0-based AI agent memory, and fixed it in one command.

The symptom: your agent "forgets" facts you stored. add() returns success. search() returns results. Retrieval benchmarks show 90%+ hit rate. But the agent can't recall specific things.

The root cause: the extraction LLM - the step that parses free text into structured facts - silently fails on smaller models. mistral:7b with the default mem0 prompt: 0% extraction recall on typed technical facts. No error. No warning.

The fix: a `custom_fact_extraction_prompt` field in the mem0 config file. Not passed to add() - that's a no-op in mem0 v1.x. Written to the config JSON, validated before applying.

After one command: 0% to 100%. Same model, same infrastructure.

This is zer0lint - open source, Apache 2.0, pip install zer0lint.

If you're building agent memory pipelines, run `zer0lint check` before you optimize retrieval. If extraction is broken, retrieval tuning doesn't help.

GitHub: https://github.com/roli-lpci/zer0lint

Hermes Labs | AI agent tooling

---
