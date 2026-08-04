# Changelog

## 0.2.3

- Add HTTP response-shape compatibility for common add/search memory APIs.
- Isolate HTTP diagnostic runs by user ID, including separate baseline and improved phases for `generate`.
- Add tests for HTTP isolation and a CI workflow across Python 3.9–3.13.
- Clarify first use, HTTP-mode limits, and the distinction between extraction diagnostics and retrieval health.
- Add release guards that require a matching `v<version>` tag, matching package metadata, expected artifacts, and a clean wheel install before PyPI publishing.

## 0.2.1

- Release universal HTTP mode.
