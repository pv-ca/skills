# Changelog

Changes a user would notice. Versions are git tags.

## Unreleased

- `gemini-web`: wrapper around your own logged-in Gemini web session (text chat, clean attached files, image generation/editing, short video, and unconfirmed Deep Research) with offline guards, per-run cookie cache isolation, and venv auto-detection. Selftest: 98/98 checks passed; evals: 6/6 passed on Claude Sonnet (low effort, dry-run, 2026-11-24).
- `gemini-web`: add `--quota` (0-credit balance check), deterministic stderr quota warnings (`>=50%`, `>=75%`, `>=90%`) and window reset times on exit 4, mode-based default `--model` (`carbon` for `image`/`video`, `hydrogen` for `chat`/`research`), `--aspect W:H` (verified full-bleed on `carbon` 16:9/9:16/4:5 and `hydrogen` 16:9), `--prompt-file` (with `openat`/`O_NOFOLLOW` symlink guards and JSON media framing), `--cookies-file` / `GEMINI_WEB_COOKIES_FILE` / default `cookies.json` fallback (for Windows App-Bound Encryption and locked keyrings, with `0600` POSIX permission checks and strict `*.google.com` filtering), swapped image/video mode hints, art-direction rules in `references/media.md`, and measured per-model image routing (`carbon`/`gemini-auto` -> `Nano Banana 2 Lite`, `hydrogen`/`neon` -> `Nano Banana 2.1`). Selftest: 221/221 checks passed (Python 3.15 and 3.12); evals: 6/6 passed on Claude Sonnet (low effort, dry-run, 2026-11-24).
- `scripts/eval.py`: add per-case fixture files (text and `base64:`, rejecting traversal and symlinks), suite/case `env`, `allow_edits`, `--effort`, and `--setting-sources project` isolation.

## 1.0.0 (2026-11-15)

- `expert`: rewrite a task the way a top professional in its field would ask for it. Moved here from `pv-ca/expert`. Evals: 4/4 passed on Claude Sonnet (2026-11-15).
