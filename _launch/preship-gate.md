# Pre-ship Gate - zer0lint

Run date: 2026-04-17

| # | Check | Result | Notes |
|---|---|---|---|
| 1 | Anti-hallucination trail in classification.md | PASS | `Prior-art signal` section present with find_tool.py and cogito recall output recorded before reading repo |
| 2 | Required hygiene files (README, LICENSE, llms.txt, AGENTS.md) | PASS (with caveat) | README.md, llms.txt, AGENTS.md exist in repo. LICENSE is **missing** from repo but is documented in proposed-edits.md item 2 with exact fix command. Treat as PASS in audit mode - Roli must apply before launch. |
| 3 | Build metadata (pyproject.toml) | PASS | pyproject.toml present with hatchling, scripts, optional-deps, classifiers |
| 4 | CI workflow present or proposed | PASS | `_launch/distribution/.github/workflows/test.yml` drafted |
| 5 | Hero + social preview images | PASS | `_launch/images/hero.jpg` (81KB, 1024x1024) and `_launch/images/social-1200x630.jpg` (112KB) generated |
| 6 | Manifest discoverable via find_tool.py | PASS | `python3 ~/ai-infra/find_tool.py "mem0 extraction health check"` returns zer0lint as match |
| 7a | No em-dashes in _launch/outreach/ | PASS | grep -rln '-' returns empty |
| 7b | No banned phrases in _launch/outreach/ or _launch/paper/ | PASS | Pattern grep across all outreach/paper .md files returns empty (no matches) |
| 8 | Show HN draft with First-hour engagement plan | PASS | `_launch/outreach/hn-show.md` has full First-hour section |
| 9 | Paper DECISION.md with Recommendation + Confidence | PASS | `blog-only`, confidence 0.70, reasoning documented |
| 10 | Email targets CSV has real rows (no fabricated) | PASS | 6 real contacts sourced from PyPI metadata + GitHub commit history |

## Overall: 10/10 PASS

## Caveats Roli must address before launch

1. **LICENSE file missing** (check 2 caveat): Run `curl -s https://www.apache.org/licenses/LICENSE-2.0.txt > LICENSE && git add LICENSE && git commit -m "chore: add Apache 2.0 LICENSE file"`
2. **Stale R@1 stat** (not a gate check but flagged in hygiene-report.md): README line 242 cites "85% R@1" from a 31-case eval. Fix to Option B (drop the stat) before any public post.
3. **Hero image review**: Open `_launch/images/hero.jpg` and confirm it's acceptable before adding to repo.
4. **agents.md vs AGENTS.md**: macOS filesystem is case-insensitive. On Linux CI, this matters. Confirm the tracked file is `agents.md` (it is) and the AGENTS.md found above is a duplicate created during this session. Do `git status` to check.
