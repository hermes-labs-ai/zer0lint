# Launch Plan - zer0lint

## T-3 days (pre-launch prep)

**Gate: hygiene done, images done, metadata applied**

- [ ] Review `_launch/proposed-edits.md` and apply approved changes to README
  - Priority 1: Fix the cogito-ergo R@1 stat (line 242) - use Option B (drop stat)
  - Priority 2: Add Table of Contents (294 lines, required)
  - Priority 3: Add `LICENSE` file (`curl -s https://www.apache.org/licenses/LICENSE-2.0.txt > LICENSE`)
  - Priority 4: Replace prose em-dashes in README body
- [ ] Run `bash _launch/gh-metadata.sh` to set GitHub topics, description, homepage
- [ ] Upload `_launch/images/social-1200x630.jpg` as the GitHub social preview
  - Go to: github.com/hermes-labs-ai/zer0lint/settings -> Social preview -> Upload image
  - This cannot be automated - must be done via GitHub web UI
- [ ] Review `_launch/images/hero.jpg` - if approved, run:
  ```bash
  mkdir -p .github/assets
  cp _launch/images/hero.jpg .github/assets/hero.jpg
  git add .github/assets/hero.jpg
  ```
  Then apply the hero image diff from proposed-edits.md item 5

**Fallback if gate fails:** If README edits are not done, do not launch. The missing LICENSE file and stale R@1 stat are the two issues that could embarrass publicly.

---

## T-2 days (content review)

**Gate: blog post reviewed by Roli**

- [ ] Read `_launch/outreach/blog-post.md` in full - verify all technical claims match current state
- [ ] Publish to DEV.to (set published: false first, preview, then toggle to published)
- [ ] Schedule Medium draft (publish same day as DEV.to, with canonical_url pointing to DEV.to)
- [ ] Check HN karma on submitting account - must have >= 50 karma to avoid shadow-hide on submit
  - If karma < 50: plan to submit via an account with more history, or build up karma first

**Fallback:** If blog post has any claims that don't match the actual repo code, fix before publishing. A wrong claim in the blog post is worse than no blog post.

---

## T-1 day (outreach prep)

**Gate: cold-email drafts reviewed (dry run only)**

- [ ] Run draft_batch.py on email-targets.csv in dry-run mode:
  ```bash
  python3 ~/ai-infra/pipeline/draft_batch.py \
    --input _launch/outreach/email-targets.csv \
    --output _launch/outreach/drafts/
  ```
- [ ] Review each draft in `_launch/outreach/drafts/` - do not send yet
- [ ] Note: the 3 mem0 team contacts (Kabir, Gabriel, Utkarsh) are current employees.
  Reaching out to them is different from reaching out to Jeff Huber or Jerry Liu.
  Consider: a more collaborative tone for mem0 team (they may want to know about extraction failures),
  a more product-pitch tone for Jeff/Jerry.

---

## T+0 (launch day)

**Gate: Tuesday/Wednesday/Thursday, 08:00-10:00 PT**

- [ ] 08:00-10:00 PT: Post Show HN using `_launch/outreach/hn-show.md`
- [ ] First-hour engagement plan activates - monitor comments, reply within 10 minutes
- [ ] Within 60 minutes of HN post: post X thread from `_launch/outreach/x-thread.md`
- [ ] Do not touch Reddit today

**Fallback:** If HN post gets <5 upvotes in first hour, do not boost artificially. Let it run. The organic signal matters more than the count.

---

## T+1 hour

- [ ] X thread posted (see above)

---

## T+1 day

- [ ] Review DEV.to and Medium - check comments, respond within 24 hours
- [ ] Post LinkedIn from `_launch/outreach/linkedin.md`

---

## T+3 days (Reddit, staggered)

**Gate: don't post to two subreddits on the same day**

- [ ] Day 1: r/Python using `_launch/outreach/reddit/r-Python.md`
- [ ] Day 2 (T+4): r/LocalLLaMA using `_launch/outreach/reddit/r-LocalLLaMA.md`

---

## T+5 days (awesome-* PRs)

- [ ] Submit PR to agarrharr/awesome-cli-apps using `_launch/outreach/awesome-prs/awesome-cli-apps.md`
- [ ] Day after: submit PR to vinta/awesome-python using `_launch/outreach/awesome-prs/awesome-python.md`

---

## T+7 days (cold email)

**Gate: email drafts reviewed and approved**

- [ ] Send cold email batch in waves of 25 via `himalaya`
- [ ] Start with Jeff Huber (Chroma) and Jerry Liu (LlamaIndex) - they are the highest-signal contacts
- [ ] mem0 team emails (3 contacts) - consider sending separately with a different angle (collaboration vs product pitch)

---

## Hard gates

1. **LICENSE file must exist** before any HN or Reddit post. GitHub without a license looks abandoned.
2. **Stale R@1 stat (85%) must be updated** before any public post. Do not publish with a stat sourced from a 31-case eval when a 470q benchmark exists.
3. **cogito-ergo must NOT be /launch-repo'd yet** per user memory: "hold on /launch-repo for cogito-ergo until Roli signals ready". zer0lint's ecosystem section should not oversell cogito-ergo's status.
