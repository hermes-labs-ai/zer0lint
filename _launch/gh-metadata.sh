#!/bin/bash
# gh-metadata.sh — run this to update GitHub repo metadata for zer0lint
# REVIEW before running. Never auto-executed.

set -e

echo "Updating zer0lint GitHub repo metadata..."

gh repo edit roli-lpci/zer0lint \
  --description "AI memory extraction diagnostics for mem0 and any HTTP memory endpoint. Hermes Labs." \
  --homepage "https://hermes-labs.ai" \
  --add-topic "mem0" \
  --add-topic "memory" \
  --add-topic "ai-agents" \
  --add-topic "diagnostics" \
  --add-topic "extraction" \
  --add-topic "llm" \
  --add-topic "python" \
  --add-topic "cli"

echo "Done. Verify at: https://github.com/roli-lpci/zer0lint"
