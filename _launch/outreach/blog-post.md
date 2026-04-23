# The Silent Failure in mem0: How We Went from 0% to 100% Extraction Recall

**Your AI agent's memory pipeline is probably lying to you.**

`add()` returns `{"results": [...]}`. `search()` returns results. Your retrieval benchmark shows 90%+ hit@any. But when you ask the agent about something you told it last week, it has no idea.

This is not a retrieval problem. It's an extraction problem. And it's completely silent.

---

## The failure mode

mem0's extraction step uses an LLM to parse free-form text into structured facts. For GPT-4 and GPT-4o, this works well. For smaller models - mistral:7b, qwen3.5:4b, llama3:8b - the default extraction prompt produces malformed JSON:

```
Error in new_retrieved_facts: Unterminated string starting at: line 1 column 10 (char 9)
Error in new_retrieved_facts: Expecting ',' delimiter: line 1 column 13 (char 12)
```

mem0 handles this gracefully by falling back to a degraded extraction or no extraction. No exception is raised. `add()` still returns success. The vector store stores something. But the specific facts you wanted to save - the ones your agent needs - are gone.

We discovered this on 2026-03-22 while running cogito-ergo (our memory server) against mistral:7b. Extraction score: 0/5 on five typed technical facts.

---

## Why it's invisible

The standard diagnostic chain fails here:

- **Check `add()` return code?** Returns success.
- **Check `search()` results?** Returns results (just not the ones you want).
- **Run a retrieval benchmark?** Shows 90%+ hit@any - because *some* things are extracted, just not the specific facts you care about.
- **Look at extraction logs?** JSON parse errors are logged but not surfaced to the caller. Easy to miss.

The only way to catch this is to inject known facts and measure whether they come back.

---

## The fix mem0 documents but doesn't make easy

mem0 has a `custom_fact_extraction_prompt` field in its config JSON. This lets you override the extraction prompt at the config level. It works. The problem: it's not prominently documented, and there's a common trap.

**The trap:** When developers figure out that extraction is broken, they try this:

```python
memory.add("The API endpoint is port 8421", prompt="Extract technical facts")
```

This has no effect in mem0 v1.x. The `prompt` parameter to `add()` does not control the extraction LLM's system prompt. No error is raised. No warning. The custom prompt is silently ignored.

The fix must go in the config:

```json
{
  "custom_fact_extraction_prompt": "You are a Technical Memory Organizer..."
}
```

But there's no built-in way to test whether your extraction prompt actually works before deploying it.

---

## zer0lint: measure, fix, validate

We built zer0lint to automate this diagnostic. It runs in three phases:

**Phase 1: Measure baseline**
```bash
zer0lint check --config ~/.mem0/config.json
```
Injects 5 synthetic technical facts (covering exact phrase, paraphrase, negation, multi-fact, entity reference), measures round-trip recall, reports a score and status.

```
Score: 0/5 (0%) - CRITICAL
  ⚠  Model upgrade: We switched from gpt-3.5-turbo to gpt-4o-mini...
  ⚠  API endpoint: The API service runs on port 8421 with TLS 1.3...
```

**Phase 2 and 3: Generate and validate a fix**
```bash
zer0lint generate --config ~/.mem0/config.json
```

Runs baseline, re-tests with zer0lint's domain-aware technical extraction prompt, and if the score improves, writes the validated prompt to `custom_fact_extraction_prompt` in your config. Backs up the original with an ISO timestamp. Only writes if improvement is confirmed.

```
[1/3] Baseline: 0/5 (0%)
[2/3] Improved: 5/5 (100%)
[3/3] Fix applied to config. Backup at ~/.mem0/config.backup.2026-03-22T02:18:34.json

Results:
  Before: 0/5 (0%)
  After:  5/5 (100%)
  Delta:  +100pp
```

Same model. Same config. One config field change.

---

## Universal HTTP mode

zer0lint also works without mem0, via HTTP:

```bash
zer0lint check --add-url http://localhost:19420/add --search-url http://localhost:19420/recall_b
```

This tests the full pipeline (ingestion + storage + retrieval) against any memory system that exposes add/search over HTTP. We use it to validate cogito-ergo's extraction layer in CI.

---

## What we learned

1. **Extraction health and retrieval health are independent.** A retrieval benchmark that looks healthy can be built entirely on degraded data. Measure extraction first.

2. **The model matters more than the prompt at small scales.** mistral:7b needed an explicit JSON-enforcing prompt. qwen3.5:4b scored 80% on the default and 100% with zer0lint's prompt. The improvement is model-dependent.

3. **`custom_fact_extraction_prompt` is the only lever.** Despite appearances, mem0 v1.x does not expose extraction customization at the call level. The config field is it.

4. **Silent failures need quantitative diagnostics.** Spot-checking one or two facts gives false confidence. You need a typed test set across multiple fact categories.

---

## Install

```bash
pip install zer0lint

# Diagnose
zer0lint check --config ~/.mem0/config.json

# Fix
zer0lint generate --config ~/.mem0/config.json
```

GitHub: https://github.com/hermes-labs-ai/zer0lint
PyPI: https://pypi.org/project/zer0lint/

zer0lint is open source (Apache 2.0) and part of the Hermes Labs agent tooling suite.
