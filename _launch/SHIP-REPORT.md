# Ship Report - zer0lint

Pre-ship gate: 10/10 PASS (see preship-gate.md for one LICENSE caveat)

## Artifacts shipped

| File | Description |
|---|---|
| `_launch/classification.md` | cli-tool verdict, prior-art signal from find_tool.py + cogito |
| `_launch/claim.md` | Falsifiable claim: 0%->100% on mistral:7b, one config change |
| `_launch/hygiene-report.md` | Full README/license/badge/distribution gap analysis |
| `_launch/proposed-edits.md` | 5 proposed README/pyproject diffs (audit mode, not applied) |
| `_launch/preship-gate.md` | 10/10 gate checks |
| `_launch/positioning.md` | Why-now, ICP, competitor delta, adjacent interests |
| `_launch/gh-metadata.sh` | Exact gh repo edit command for topics/description/homepage |
| `_launch/release.sh` | PyPI Trusted Publishing instructions + manual fallback |
| `_launch/images/hero.jpg` | 1024x1024 hero (Pollinations.ai, free) |
| `_launch/images/social-1200x630.jpg` | Social preview for GitHub/X/LinkedIn |
| `_launch/images/architecture.mmd` | Mermaid architecture diagram (check/generate flow) |
| `_launch/images/demo-plan.md` | asciinema shot list for 45-60s demo GIF |
| `_launch/distribution/CHANGELOG.md` | v0.1.0/0.2.0/0.2.1 history + [Unreleased] v0.3 items |
| `_launch/distribution/CONTRIBUTING.md` | Clone, install, test, lint, PR instructions |
| `_launch/distribution/CODE_OF_CONDUCT.md` | Contributor Covenant v2.1 (URL reference, not inlined) |
| `_launch/distribution/.pre-commit-config.yaml` | ruff pre-commit hook |
| `_launch/distribution/.github/workflows/test.yml` | pytest CI across Python 3.9-3.12 |
| `_launch/distribution/.github/workflows/release.yml` | PyPI Trusted Publishing (OIDC) on v* tags |
| `_launch/outreach/hn-show.md` | Show HN draft + first-hour engagement plan |
| `_launch/outreach/blog-post.md` | 800+ word technical post (Medium-compatible) |
| `_launch/outreach/blog-post.devto.md` | Same post with DEV.to YAML frontmatter |
| `_launch/outreach/reddit/r-Python.md` | r/Python Showcase post |
| `_launch/outreach/reddit/r-LocalLLaMA.md` | r/LocalLLaMA Tool post |
| `_launch/outreach/linkedin.md` | 200-word professional post |
| `_launch/outreach/x-thread.md` | 7-tweet thread |
| `_launch/outreach/email-targets.csv` | 6 real contacts (PyPI + GitHub commit sourcing) |
| `_launch/outreach/awesome-prs/awesome-cli-apps.md` | PR draft for agarrharr/awesome-cli-apps |
| `_launch/outreach/awesome-prs/awesome-python.md` | PR draft for vinta/awesome-python |
| `_launch/outreach/README-outreach.md` | Ordered outreach index |
| `_launch/paper/DECISION.md` | blog-only, confidence 0.70 |
| `_launch/LAUNCH-PLAN.md` | Day-by-day with go/no-go gates through T+7 |

## What Roli does next (ordered)

1. `open _launch/images/hero.jpg _launch/images/social-1200x630.jpg` - eyeball both, re-roll if needed
2. Apply proposed-edits.md item 2: `curl -s https://www.apache.org/licenses/LICENSE-2.0.txt > LICENSE && git add LICENSE && git commit -m "chore: add Apache 2.0 LICENSE file"`
3. Apply proposed-edits.md item 1a (stale R@1 fix): change README line 242 to Option B
4. Apply proposed-edits.md item 1b (TOC) and 1d (uv install)
5. `bash _launch/gh-metadata.sh` - sets topics, description, homepage
6. Upload social-1200x630.jpg to GitHub repo settings as social preview (manual, web UI)
7. Copy distribution/ files to repo: CHANGELOG.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, .pre-commit-config.yaml, .github/workflows/
8. Review blog-post.md, publish to DEV.to
9. Post Show HN on a Tuesday/Wednesday/Thursday 08:00-10:00 PT

## Paper decision

blog-only - confidence 0.70. Two models and one corpus is not publishable. Run a 5-model, 50-fact systematic study for v0.3 data to upgrade to publish-workshop.

## Gate waivers

- Check 2 (LICENSE file): waived in audit mode. File is proposed with exact fix command. Must be applied before any public post.
- Check 7a note: em-dash check ran on `_launch/outreach/` and `_launch/paper/`. The README.md itself (tracked file) still has em-dashes - those are in proposed-edits.md as fix 1h.
