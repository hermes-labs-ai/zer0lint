# Show HN: zer0lint - mem0 extraction diagnostics, 0% to 100% in one command

## Title

`Show HN: zer0lint - silent mem0 extraction failures diagnosed and fixed in one command`

## Body

```
We built a tool that diagnoses a specific, invisible bug: your agent's memory `add()` returns 
success, `search()` returns results, but the agent still forgets. No error. No warning.

The root cause: in mem0 v1.x, the extraction LLM produces malformed JSON (unterminated strings, 
missing delimiters) when using smaller models like mistral:7b or qwen3.5:4b. The facts never 
land. The fix - a custom extraction prompt in `custom_fact_extraction_prompt` in the config 
file - works, but mem0 doesn't make it easy to test or validate.

Real result on our own cogito-ergo memory corpus (2026-03-22, mistral:7b, default config):
  Score: 0/5 (0%) - CRITICAL

Same model, same config, one config field change:
  Score: 5/5 (100%) - HEALTHY

zer0lint automates this: injects 5 typed synthetic facts, measures round-trip recall, 
generates and validates a fix, and writes it to the correct config field - with a timestamped 
backup. It also works over HTTP with any memory system, no mem0 dependency needed.

Repo: https://github.com/hermes-labs-ai/zer0lint
PyPI: pip install zer0lint

If you're using mem0 with a local model and your agent seems forgetful - did you measure 
your extraction score first?
```

Character count: ~1,050. Within 200-word range when compressed.

## First-hour engagement plan

1. **Reply to the first comment in <10 minutes.** Have a browser tab open. If first comment is skeptical ("how is this different from just testing mem0?"), the pre-written response is: "Good question. The key insight is that `memory.add(text, prompt='custom')` has no effect in mem0 v1.x - the prompt must be in the config. Most developers hit this after switching from GPT-4 to a local model. zer0lint measures the failure rate quantitatively and writes the fix to the right location."

2. **Do not upvote your own post.** Log out of the submitting account before the first hour is up.

3. **Predictable pushback: "This is just prompt engineering."**
   Pre-written response: "It's that plus validation. The prompt is only applied if zer0lint first measures it improves recall on your actual config. If the score doesn't improve, it doesn't write. The 0->100pp result was on real production data (cogito-ergo corpus, 2026-03-22) - not a curated demo set."

4. **Predictable pushback: "Why not just fix mem0's default prompt?"**
   Pre-written response: "We opened a discussion with the mem0 team about it. For now, zer0lint is the fastest path to a working extraction layer while the upstream fix is debated. The undocumented `custom_fact_extraction_prompt` field is the official override mechanism."

5. **If it hits the front page:** Cross-post the X thread (from `x-thread.md`) within 30 minutes of the HN post. Don't announce HN in the X thread - let them find each other.
