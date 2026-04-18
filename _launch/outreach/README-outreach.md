# Outreach Bundle - zer0lint

Do these in this order.

---

## Step 1: Blog post (T-2 days)

Review and optionally publish these drafts before anything else. The blog post is the canonical long-form content all other outreach links back to.

- `blog-post.md` - Medium-compatible, 800-1200 words, technical
- `blog-post.devto.md` - Same content, DEV.to YAML frontmatter included, set `published: false`

**Action:** Review, publish to DEV.to first (canonical_url already set to GitHub), then Medium.

---

## Step 2: GitHub metadata (T-2 days)

```bash
bash _launch/gh-metadata.sh
```

Sets description, homepage (hermes-labs.ai), and 8 topics. Run once, done.

---

## Step 3: Show HN (T+0, launch day, 08:00-10:00 PT)

- `hn-show.md` - Full HN post with title, body, and first-hour engagement plan

**Action:** Post manually. First-hour plan: reply to first comment <10 min, don't upvote self, have 3 pre-written responses ready (all in hn-show.md).

---

## Step 4: X thread (T+0, within 60 minutes of HN post)

- `x-thread.md` - 7-tweet thread, hook first, numbers in tweet 5

**Action:** Post thread. Do not reference HN post in the thread.

---

## Step 5: LinkedIn (T+1 day)

- `linkedin.md` - 150-250 words, professional framing, no emoji

**Action:** Post directly. Consider tagging Hermes Labs page if the account is set up.

---

## Step 6: Reddit (T+3 days, staggered)

- `reddit/r-Python.md` - r/Python with Showcase flair
- `reddit/r-LocalLLaMA.md` - r/LocalLLaMA with Tool flair

**Action:** Post one per day, 24 hours apart. Do not cross-post on the same day.

---

## Step 7: Awesome-* list PRs (T+3 to T+7)

- `awesome-prs/awesome-cli-apps.md` - PR to agarrharr/awesome-cli-apps
- `awesome-prs/awesome-python.md` - PR to vinta/awesome-python

**Action:** Submit each PR manually following the instructions in each file.

---

## Step 8: Direct outreach (T+7 days)

- `email-targets.csv` - 6 real contacts from PyPI metadata and GitHub commit history

Run the draft pipeline:
```bash
python3 ~/ai-infra/pipeline/draft_batch.py \
  --input _launch/outreach/email-targets.csv \
  --output _launch/outreach/drafts/
```

Review each draft before sending. Send in waves of 25 via himalaya.

---

## Contacts summary

6 real contacts sourced from:
- `npm_email_extract.py --registry pypi` on mem0ai, chromadb, llama-index
- `gh_commit_check.py` on mem0ai/mem0 repo

Contacts: Jeff Huber (Chroma), Jerry Liu (LlamaIndex), Andrei Fajardo (LlamaIndex), Kabir Kohli (Mem0), Gabriel Stein (Mem0), Utkarsh Kumar (Mem0).

No placeholder or fabricated rows. All sourced from public PyPI author fields or GitHub commit emails.
