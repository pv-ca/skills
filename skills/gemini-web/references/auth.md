# Authentication

`scripts/gemini_web.py` has no login of its own. It reads the Google cookies of a browser where you are
already logged in to gemini.google.com, using `browser-cookie3`, and hands them to `gemini-webapi`.

## How it works

1. `load_cookies` asks each supported browser in turn (Edge, Chrome, Chromium, Brave, Firefox, Vivaldi,
   Opera, LibreWolf) for the cookies of `google.com`, and takes the first browser that holds a
   `__Secure-1PSID` cookie. `--browser NAME` or `GEMINI_WEB_BROWSER` selects one.
2. `make_client` builds the `gemini-webapi` client from the two session cookies and then loads the whole
   Google cookie jar into it. With only the two session cookies, `init()` timed out in testing; with the
   whole jar it worked.
3. Cookie values are never printed or written to the call log (`~/.local/share/gemini-web/calls.jsonl`, mode `0600`).
4. By default `gemini-webapi` caches cookies under `/tmp/gemini_webapi/` using `__Secure-1PSID` in the filename, and tries cached cookies before caller-supplied ones (which can shadow fresh browser cookies with a stale session). `scripts/gemini_web.py` overrides `GEMINI_COOKIE_PATH` to a fresh private `0700` temporary directory for each run and removes it on exit.

## Python environment

If the active `python3` lacks `gemini-webapi`, `browser-cookie3`, or `curl_cffi`, `scripts/gemini_web.py` automatically re-execs into the first executable interpreter found in:

1. `$GEMINI_WEB_PYTHON`
2. `<skill-dir>/.venv/bin/python` (or `Scripts/python.exe`)
3. `$XDG_DATA_HOME/gemini-web/venv/bin/python` (default `~/.local/share/gemini-web/venv/bin/python`)

## If it fails (exit code 2)

- "no browser with a logged-in Google session found": open gemini.google.com in a supported browser and
  log in, or pass `--browser`.
- "missing dependency": install `requirements.txt` into `~/.local/share/gemini-web/venv` (or `.venv/`), or set `GEMINI_WEB_PYTHON`.
- The browser is open and logged in but nothing is found: on Linux the cookie store may need the desktop
  keyring unlocked; `browser-cookie3` documents which browsers and platforms it supports.
- An authentication error after it used to work: the session expired. Log in again in the browser.

## The pinned library

`requirements.txt` pins `gemini-webapi==2.1.1`. The `medium` effort level rewrites a private part of the
request that this exact version builds, and the model label check reads the raw response. After raising
the version, run `--selftest`, then one cheap call at each effort level and check that the label appears
and the exit code is 0. The library is released under the AGPL-3.0, which matters if you redistribute
anything that includes it.

## Notes

- This drives an unofficial web interface. Google can change it without notice, and using it may fall
  outside what Google's terms allow for automated access. You use your own account at your own risk.
- The session cookies give full access to the Google account. Keep them out of logs, prompts, issues and
  commits. If one leaks, sign out of all sessions in the Google account settings.
