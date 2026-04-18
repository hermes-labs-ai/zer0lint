---
title: "The Silent Failure in mem0: How We Went from 0% to 100% Extraction Recall"
published: false
tags: [mem0, ai, python, agents]
canonical_url: https://github.com/roli-lpci/zer0lint
---

Your AI agent's memory pipeline is probably lying to you.

`add()` returns success. `search()` returns results. Your retrieval benchmark shows 90%+ hit@any. But when you ask the agent about something you told it last week, it has no idea.

This is not a retrieval problem. It's an extraction problem. And it's completely silent.

---

## The failure mode

mem0's extraction step uses an LLM to parse free-form text into structured facts. For GPT-4 and GPT-4o, this works well. For smaller models - mistral:7b, qwen3.5:4b, llama3:8b - the default extraction prompt produces malformed JSON:

```
Error in new_retrieved_facts: Unterminated string starting at: line 1 column 10 (char 9)
Error in new_retrieved_facts: Expecting ',' delimiter: line 1 column 13 (char 12)
```

mem0 handles this gracefully by falling back to degraded extraction. No exception. `add()` returns success. The facts are gone.

---

## Why it's invisible

The standard diagnostic chain fails here:

- **Check `add()` return code?** Returns success.
- **Check `search()` results?** Returns results (just not the right ones).
- **Run a retrieval benchmark?** Shows 90%+ hit@any.
- **Look at extraction logs?** JSON parse errors logged but not surfaced.

The only way to catch this: inject known facts and measure whether they come back.

---

## The fix mem0 documents but doesn't make easy

mem0 has `custom_fact_extraction_prompt` in its config JSON. It works. But there's a trap many developers hit:

```python
# This has NO EFFECT in mem0 v1.x
memory.add("The API is on port 8421", prompt="Extract technical facts")
```

The `prompt` parameter to `add()` does not control extraction in mem0 v1.x. No error, no warning, no effect. The fix goes in the config:

```json
{
  "custom_fact_extraction_prompt": "You are a Technical Memory Organizer..."
}
```

---

## zer0lint: measure, fix, validate

```bash
pip install zer0lint

# Measure
zer0lint check --config ~/.mem0/config.json
# Score: 0/5 (0%) - CRITICAL

# Fix
zer0lint generate --config ~/.mem0/config.json
# Before: 0/5 (0%) | After: 5/5 (100%) | Delta: +100pp
```

Injects 5 typed synthetic facts, measures round-trip recall, generates a validated extraction prompt, writes it to the correct config field with a timestamped backup.

Real result on the cogito-ergo production corpus (2026-03-22, mistral:7b): 0% to 100% in one command.

Also works over HTTP with any memory system:

```bash
zer0lint check --add-url http://localhost:19420/add --search-url http://localhost:19420/recall_b
```

---

## The key lesson

Extraction health and retrieval health are independent. A retrieval benchmark that looks healthy can be built on degraded data. Measure extraction first, before tuning retrieval.

GitHub: https://github.com/roli-lpci/zer0lint
PyPI: `pip install zer0lint`
Apache 2.0. Hermes Labs.
