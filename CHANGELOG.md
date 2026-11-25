# Changelog

Changes a user would notice. Versions are git tags.

## Unreleased

- `gemini-web`: wrapper around your own logged-in Gemini web session (text chat, clean attached files, image generation/editing, short video, and unconfirmed Deep Research) with offline guards, per-run cookie cache isolation, and venv auto-detection. Selftest: 98/98 checks passed; evals: 6/6 passed on Claude Sonnet (low effort, dry-run, 2026-11-24).
- `scripts/eval.py`: add per-case fixture files (text and `base64:`, rejecting traversal and symlinks), suite/case `env`, `allow_edits`, `--effort`, and `--setting-sources project` isolation.

## 1.0.0 (2026-11-15)

- `expert`: rewrite a task the way a top professional in its field would ask for it. Moved here from `pv-ca/expert`. Evals: 4/4 passed on Claude Sonnet (2026-11-15).
