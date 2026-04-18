# Proposed Edits - zer0lint (AUDIT MODE)

Apply via `git apply _launch/fixes.patch` or manually. All changes are proposals - do NOT apply without review.

---

## 1. README.md - Critical fixes

### 1a. Fix stale cogito-ergo R@1 stat (THE KNOWN BUG)

Current line 242:
```
Deploy retrieval           ->  cogito-ergo (two-stage retrieval, 85% R@1)
```

Problem: 85% comes from a 31-case internal eval (2026-03-28). LongMemEval 470q benchmark (2026-04-15) shows 83.2% R@1 for the combined system; 89% with latest polish (not yet published). Cogito-ergo is also not yet publicly launched with these benchmarks.

**Proposed fix (option A - use verified number):**
```
Deploy retrieval           ->  cogito-ergo (two-stage retrieval, 83%+ R@1 on LongMemEval)
```

**Proposed fix (option B - drop the stat until cogito-ergo launches):**
```
Deploy retrieval           ->  cogito-ergo (two-stage retrieval, local)
```

Recommendation: Option B. zer0lint's README should not carry forward a benchmark from a repo not yet publicly launched.

---

### 1b. Add Table of Contents (294 lines, >200 threshold)

Insert after the badge block, before "Is this you?":

```markdown
## Contents

- [Is this you?](#is-this-you)
- [The Problem](#the-problem)
- [Quick Start](#quick-start)
- [What It Does](#what-it-does)
- [Critical Discovery](#critical-discovery-where-extraction-actually-happens)
- [Config Format](#config-format)
- [Test Results](#test-results-2026-03-22)
- [How It Works](#how-it-works)
- [Ecosystem](#ecosystem)
- [Installation](#installation)
- [Supported Systems](#supported-systems)
- [License](#license)
```

---

### 1c. Convert bold tagline to blockquote

Current (line 3):
```markdown
**AI memory extraction diagnostics.** Your agent seems forgetful - zer0lint finds the root cause and fixes it in one command.
```

Proposed:
```markdown
> Diagnoses silent mem0 extraction failures and fixes them in one command.
```

(The current tagline is clear but uses bold paragraph, not `>` blockquote per spec.)

---

### 1d. Add uv install path

Current Quick Start only shows `pip install zer0lint`. Add:
```bash
pip install zer0lint       # standard
uv tool install zer0lint   # faster, isolated
```

---

### 1e. Add downloads badge

Current badge block (line 5-8) is missing a downloads badge. Add after the license badge:
```markdown
[![Downloads](https://img.shields.io/pypi/dm/zer0lint)](https://pypi.org/project/zer0lint/)
```

---

### 1f. Fix license line

Current last section:
```markdown
## License

Apache 2.0
```

Proposed:
```markdown
## License

Apache 2.0 - see [LICENSE](LICENSE).
```

(Also requires adding the LICENSE file - see item 2 below.)

---

### 1g. Add "vs alternatives" section

Insert before Installation:

```markdown
## vs Alternatives

| Approach | What it does | Where zer0lint wins |
|---|---|---|
| Manual spot-checking | Developer manually adds a fact and searches for it | zer0lint automates 5 test cases across 5 domains, gives a score, and generates a fix |
| mem0 debug logs | Read JSON parse errors directly | Logs show the symptom; zer0lint shows the score and applies a validated fix |
| Custom extraction prompt via add() | Pass prompt at call time | In mem0 v1.x this has zero effect. zer0lint writes to the correct config field. |
| No diagnostics | Assume extraction works | Silent failure is the default. zer0lint is the only automated tool that measures it. |
```

---

### 1h. Fix prose em-dashes

The README contains 11+ em-dashes in prose (excluding code blocks). These violate voice rules. Examples:

- Line 3: `forgetful - zer0lint` -> `forgetful. zer0lint`
- Line 16: `benchmark - numbers look` -> `benchmark, numbers look`
- Line 31: `never land - degraded fallbacks` -> `never land. Degraded fallbacks`

Full sed replacement for prose em-dashes (apply carefully, code blocks use em-dashes in CLI output and should be preserved verbatim - they are not README prose):

Note: The em-dashes inside ``` code blocks ``` are program output, not README prose. Only fix the prose em-dashes listed in hygiene-report.md.

---

## 2. LICENSE file (missing - critical)

The repo has no `LICENSE` file. pyproject.toml declares `license = {text = "Apache-2.0"}` but GitHub cannot display the license without the file.

**Action:** Add `LICENSE` file with Apache 2.0 full text. Get it from:
```bash
curl -s https://www.apache.org/licenses/LICENSE-2.0.txt > LICENSE
git add LICENSE && git commit -m "chore: add Apache 2.0 LICENSE file"
```

---

## 3. agents.md -> AGENTS.md (rename)

Current: `agents.md` (lowercase)
Standard: `AGENTS.md` (uppercase, matches Claude Code convention)

```bash
git mv agents.md AGENTS.md
git commit -m "chore: rename agents.md to AGENTS.md per convention"
```

---

## 4. pyproject.toml - add Rolando Bosch as author

Current:
```toml
authors = [
    {name = "Hermes Labs", email = "roli@hermes-labs.ai"},
]
```

Proposed (add individual author alongside org):
```toml
authors = [
    {name = "Rolando Bosch", email = "rbosch@lpci.ai"},
    {name = "Hermes Labs", email = "roli@hermes-labs.ai"},
]
```

Reason: PyPI shows the author name prominently. "Hermes Labs" as author is valid, but having Rolando's name helps with discoverability and matches the Hermes handbook convention.

---

## 5. Hero image (after Phase 2 generation)

Once `_launch/images/hero.jpg` is reviewed and approved:

```markdown
<!-- Insert at top of README, above # zer0lint -->
<p align="center">
  <img src=".github/assets/hero.jpg" alt="zer0lint - AI memory extraction diagnostics" width="720">
</p>
```

Copy the file:
```bash
mkdir -p .github/assets
cp _launch/images/hero.jpg .github/assets/hero.jpg
```
