# Claim - zer0lint

## The claim

**zer0lint diagnoses silent mem0 extraction failures - the ones where `add()` succeeds and `search()` returns results, but the agent still forgets - and fixes them in one command by writing a validated extraction prompt to the correct config field.**

### Falsifiable form

A mem0 instance running mistral:7b with default config scores 0/5 (0%) on zer0lint's synthetic fact injection test. After running `zer0lint generate`, the same instance scores 5/5 (100%). No other changes. Repeatable.

### Evidence base

Empirical result from 2026-03-22 logged in README and `llms.txt`:
- mistral:7b default prompt: 0/5 (0%) - CRITICAL
- mistral:7b with zer0lint prompt: 5/5 (100%) - HEALTHY
- Delta: +100 percentage points

## Audience

AI engineers and agent developers who use mem0 (or any HTTP-accessible memory system) and have hit the silent extraction failure pattern - where the memory pipeline returns success codes but the agent cannot recall stored facts.

## Key insight surfaced

In mem0 v1.x, passing a custom prompt via `memory.add(..., prompt=X)` has no effect on extraction quality. The extraction prompt must live in `custom_fact_extraction_prompt` in the config file. This is undocumented. zer0lint finds this failure, proves it, and writes the fix to the correct location.
