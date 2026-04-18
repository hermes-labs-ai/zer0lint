# Demo GIF Plan - zer0lint

Target: 45-60 seconds. Shows the full 0->100% journey in one take.

## Prerequisites

Have a running mem0 instance with mistral:7b or any local Ollama model that produces low scores with default config.

## Recording recipe

```bash
brew install asciinema agg
asciinema rec demo.cast --title "zer0lint: 0% to 100% in 90 seconds"
# record the session below
# when done: Ctrl+D
agg demo.cast demo.gif --font-size 14 --cols 100 --rows 30
```

Place at: `.github/assets/demo.gif`
Embed in README above the Quick Start section:
```markdown
<img src=".github/assets/demo.gif" alt="zer0lint demo: 0% to 100%" width="720">
```

## Shot list (type these verbatim)

**Step 1: Show the problem (10 seconds)**
```bash
zer0lint check --config ~/.mem0/config.json
```
Wait for output. Shows: `Score: 0/5 (0%) - CRITICAL`

Pause 2 seconds on the output.

**Step 2: One command fix (30 seconds)**
```bash
zer0lint generate --config ~/.mem0/config.json
```
Let it run all 3 phases. Shows:
- `[1/3] Baseline: 0/5 (0%)`
- `[2/3] Improved: 5/5 (100%)`
- `[3/3] Fix applied to config`

Pause 2 seconds on the Results block showing `Before: 0% After: 100% Delta: +100pp`

**Step 3: Confirm (10 seconds)**
```bash
zer0lint check --config ~/.mem0/config.json
```
Shows: `Score: 5/5 (100%) - HEALTHY`

## Tips

- Use a terminal with dark background (matches hero image palette)
- Set font to a monospace that renders checkmarks and warning symbols correctly (Fira Code, JetBrains Mono)
- Slow down typing slightly so viewers can read commands
- `asciinema` records at actual speed - no need to fake pauses
