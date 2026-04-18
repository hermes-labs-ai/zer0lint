#!/bin/bash
# zer0lint release script — DO NOT RUN WITHOUT REVIEW
# Preferred path: use PyPI Trusted Publishing (OIDC) via GitHub Actions release.yml
# Manual fallback only if OIDC is not configured.

set -e

echo "=== zer0lint release ==="
echo ""
echo "PREFERRED: Push a version tag to trigger the GitHub Actions release workflow:"
echo ""
echo "  git tag v0.3.0"
echo "  git push origin v0.3.0"
echo ""
echo "This triggers .github/workflows/release.yml which publishes via PyPI Trusted Publishing (OIDC)."
echo "No long-lived API tokens stored in secrets."
echo ""
echo "To configure Trusted Publishing on PyPI:"
echo "  https://pypi.org/manage/project/zer0lint/settings/publishing/"
echo "  Publisher: GitHub Actions"
echo "  Repo: roli-lpci/zer0lint"
echo "  Workflow: release.yml"
echo ""
echo "--- MANUAL FALLBACK (only if OIDC not configured) ---"
echo ""
echo "Requires: pip install build twine"
echo ""
echo "  python -m build"
echo "  python -m twine upload dist/*"
echo ""
echo "Note: twine will prompt for PyPI credentials."
echo "Store credentials in ~/.pypirc or use TWINE_USERNAME/TWINE_PASSWORD env vars."
