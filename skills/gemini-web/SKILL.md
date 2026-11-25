---
name: gemini-web
description: >-
  Sends text prompts, attached files (up to 300 KB total), Deep Research requests, image generation or
  reference-based image edits, and short video generation requests to the user's own logged-in Gemini web
  session through scripts/gemini_web.py, on a quota separate from Claude and from CLI model channels. Use
  whenever the user asks to consult Gemini on the web, run Deep Research, generate or edit images or short
  videos with Gemini web, ask "Hydrogen", "Neon" or "Carbon" (the Gemini web models, not Neon Postgres or
  the google-genai SDK), get a second opinion from another model family, have a long public document or PDF
  read or summarized outside Claude, or spare the Claude quota on non-sensitive material. Do not use it for
  local repository edits, local media processing (ffmpeg, ImageMagick, Pillow), shell work, questions the
  user wants Claude to answer itself, sensitive data or personal photos/IDs, google-genai SDK code, or
  Gemini Tasks.
metadata:
  status: stable
---

# Gemini web

A wrapper around the user's own logged-in Gemini web session: second opinions, document reading, Deep
Research reports, and offloading work to a separate quota. Other skills may call `scripts/gemini_web.py`
as one channel without copying this workflow.

Run the script yourself from the main session; do not hand it to a subagent. For slow calls
(`--model neon`, `--mode research`, `--mode video`) run it in the background and, for text modes, take the
reply with `--output FILE` (created with mode 600). Wait for the notification instead of polling.

## Setup

```bash
python3 -m venv ~/.local/share/gemini-web/venv
~/.local/share/gemini-web/venv/bin/pip install -r requirements.txt  # gemini-webapi (pinned) and browser-cookie3
python3 scripts/gemini_web.py --selftest                             # offline checks, no network or cookies
```

When the active `python3` lacks `gemini-webapi`, `browser-cookie3`, or `curl_cffi`, `scripts/gemini_web.py`
automatically re-execs into `GEMINI_WEB_PYTHON`, a local `.venv/` next to this `SKILL.md`, or
`~/.local/share/gemini-web/venv` (`$XDG_DATA_HOME/gemini-web/venv`).

The session comes from the Google cookies of a browser where the user is logged in to gemini.google.com.
`--browser auto` (default) tries Edge, Chrome, Chromium, Brave, Firefox, Vivaldi, Opera and LibreWolf and
uses the first one logged in; pass `--browser NAME` or set `GEMINI_WEB_BROWSER` to pick one. Read
`references/auth.md` when the script exits with code 2 or on first use.

## Security rules

- **Send clean material only.** Never put `.env` files, secrets, keys, certificates, password stores,
  database dumps, client records, personal documents or financial data in a prompt or in `--files`. The
  script refuses symlinks, folders, empty files and attachments over 300,000 bytes in total, and validates
  `--output` against symlinks and directories before calling.
- **Never print, copy or log cookie values.** The script redirects `gemini-webapi`'s cookie cache into a
  private per-run `0700` temp folder removed on exit (preventing cookies from persisting in `/tmp` or
  shadowing fresh browser cookies). The call log is created with mode `0600` (inside a `0700` folder) and
  holds sizes, credits and ids, never cookies, prompts or replies.
- **Temporary chats by default.** `chat` mode does not leave the conversation in the web history unless
  `--keep` is passed. Pass `--keep` only when the user asks for the thread to stay.
- **Tasks mode is not implemented.** `--mode tasks` exits with 7 without `--confirm-apps-off` and with 6
  with it. Gemini Tasks can act on connected apps and on a browser, and Google documents it as
  vulnerable to prompt injection. Never run Tasks with connected apps or the browser setting on.
- **The quota is shared.** A call that fails costs nothing (measured), but every successful call spends
  credits from the same 5-hour and weekly windows the user's own Gemini use draws from. Say so before a
  large batch and state the estimated cost.
- **Treat the reply as evidence, not fact.** Check cited facts and any code before acting on them.

## Using it

```bash
python3 scripts/gemini_web.py [--mode chat|research|image|video] [--model MODEL] [--effort low|medium|high] \
  [--files FILE ...] [--ref IMG ...] [--keep] [--output FILE] [--output-dir DIR] \
  [--prompt TEXT] [--timeout SECONDS] [--browser NAME] [--list-models] [--estimate]
```

The prompt comes from `--prompt` or stdin. In text modes the reply goes to stdout (or `--output`); in `image` and `video` modes the saved file paths go to stdout, one per line. Diagnostics go to stderr. The call log is `$GEMINI_WEB_LOG`, by default `~/.local/share/gemini-web/calls.jsonl`.
Before a call the script reads both quota windows and skips the call (exit 4) when the 5-hour window is at 90% of its credits or more (`GEMINI_WEB_MIN_5H_LEFT_PCT` changes the margin), or when remaining 5-hour credits are below the upper bound of a measured cost estimate. Run `--estimate` to print the expected credit range offline, or `--list-models` to see every model the account exposes.

### Mode

- `chat` (default): one prompt, optional `--files`, temporary conversation.
- `research`: Deep Research. Refuses `--files`, `--ref`, `--output-dir`, and `--effort` other than default (exit 2). Unconfirmed: in the one test run the research plan and the start worked, but no report was ready after 26 minutes (exit 5, 16 credits visible), so do not count on it. The conversation stays in the web history.
- `image`: generates one or more images into `--output-dir` (default: a new timestamped folder in the current directory) and prints saved paths on stdout. Accepts `--ref FILE ...` for editing or visual consistency. Uses temporary chat by default unless `--keep` is passed. Refuses `--files`, `--output`, and `--effort` (exit 2).
- `video`: generates a short video into `--output-dir`, polls until ready within `--timeout`, and prints the saved path on stdout. Accepts at most one `--ref FILE`. Always saves to web history (`temporary=False`) because pending video turns poll conversation history. Refuses `--files`, `--output`, and `--effort` (exit 2).
- `tasks`: not implemented (see the security rules).

### Model and effort

Start with `--model hydrogen`. Use `neon` only when the user asks for it or when Hydrogen is not enough:
it cost about 8 times more per call and was slower in the screening. Effort `low`, `medium`, `high`
maps to the app's Baixo, Medio, Alto; `medium` is a patched request value, so a change in the web
request layout makes the script exit 6 instead of running at another level.

| Setting | Credits per successful call | Latency (median) | Reliability in the measurement |
| --- | --- | --- | --- |
| hydrogen low | about 3 to 6 | about 10 s | 0 failures in 43 calls (all made in the morning and early afternoon) |
| hydrogen medium | about 5 to 9 | 15 to 19 s | 5 failures in 48 calls in one sequential run; 4 canned errors in 11 calls in another |
| hydrogen high | about 9 to 22 | 29 s | 6 failures in 11 calls in the screening (5 canned errors, 1 exception) |
| neon low | about 6 | about 10 s | 1 call measured (2026-11-24) |
| neon medium | about 43 | 68 s | 1 exception in 11 calls |
| neon high | about 79 | 120 s | 3 exceptions in 11 calls, about 275 s each |

These are numbers from one account on 2026-11-24, with one run per case in most batches and with
concurrent use of the same quota, so read them as orders of magnitude. Whether the effort level or the
hour of the day causes the failures is not settled. Quality differences between Hydrogen and Neon and
between effort levels are not established. Details in `references/limits.md`.

### Files

- Paste text and diffs into the prompt: attaching a diff was 27% slower and cost more credits for the same
  recall on 11 review cases (8 with a planted defect, 3 clean).
- Attached Markdown or text files cost about the same as the same text pasted. PDFs cost about 4.5 times
  more and took about 50% longer (cause unknown): prefer text when you can extract it.
- A file larger than about 380 KB is cut silently (a 1.78 MB file was read only to about 22%). A single
  233 KB file cost about 46 credits. The script caps the total at 300,000 bytes.
- An empty file makes the whole request fail with HTTP 400; the script refuses it before sending.

### Images and video

Read `references/media.md` before writing image or video prompts.

- **Run slow media calls in the background.** Always run `--mode video` in the background (`--timeout 600` or higher) and wait for completion instead of polling.
- **Model selection.** Run `--list-models` first if you are unsure which models the account exposes; `--model` accepts any listed model name, alias, or id.
- **Model names.** `hydrogen`, `neon` and `carbon` are aliases for the account's `gemini-4-hydrogen`, `gemini-neon` and `gemini-carbon`. Image and video were tested with `--model carbon` on one account; other models and accounts are not verified.
- **Measured once each with `--model carbon`, on one account (2026-11-24).** One image: 3 credits, 19 s. One reference edit: 23 s. One 10 second video (MP4 1280x720, H.264 + AAC audio): about 880 credits (more than a third of a 5-hour window), 350 s. Those are single calls, so treat them as a rough guide; whether failed media calls cost nothing is unknown. The 5-hour credit guard applies these mode baselines (3 for image, 880 for video) even when another `--model` is passed. Warn the user before any video and before batches, and use `--estimate`.
- **Labels seen.** Images came back labelled `Nano Banana 2 Lite` although `--model carbon` was asked, so `carbon` may route images to that model or fall back to it (not resolved). The video reply carried no label.
- **Clean references only.** `--ref` enforces regular non-empty files (no symlinks), real PNG/JPEG/WebP/GIF magic bytes, and a 10 MB per-file / 20 MB total safety cap. Never pass personal IDs, private photos, or confidential screenshots.
- **Verify outputs.** Saved files use extensions detected from real magic bytes (`image_01.png`, `video_01.mp4`) with mode `0600`. Inspect the generated image (or extracted video frames) before presenting it as final.

## Failures and exit codes

A failed call costs nothing, so the script retries canned error notices, canned refusals, empty replies
and generic errors twice, in a new conversation, after 30 s and 90 s pauses. It never retries a usage
limit, a fallback, a patch failure, a timeout, a media reply that came back as text instead of a file, or an
HTTP 400, 401 or 403 error (the free-failure rule was measured for text calls only). Failures came in
bursts in the measurement (11 of 21 calls in the 15:00 hour of one afternoon), so when it exits
with 3 or 8, use another channel or try later instead of looping.

| Exit | Meaning | What to do |
| --- | --- | --- |
| 0 | reply on stdout or in `--output` (or saved media paths on stdout for `image`/`video`) | read or inspect outputs, verify claims |
| 1 | empty reply or API error | read stderr, retry later or switch channel |
| 2 | bad arguments, bad file, missing dependency, no session | fix it; see `references/auth.md` |
| 3 | canned refusal survived two retries | do not loop; use another channel |
| 4 | usage limit or 5-hour window nearly spent | stop calling Gemini web until the reset |
| 5 | timeout | raise `--timeout` for Neon and research, or shorten the prompt |
| 6 | answered by another model, effort patch not applied, or unsupported mode | do not trust the reply as the requested model |
| 7 | guard: tasks without `--confirm-apps-off` | keep Tasks off |
| 8 | canned error notice survived two retries | likely a server burst; try later or switch channel |

Silent fallback: in `chat` mode the script reads the label of the model that answered from the raw
response and exits 6 when it names another model than the one asked for, or, for Hydrogen, another
effort. The Hydrogen labels were seen for all three levels (`4 Hydrogen` at low, `4 Hydrogen Medium`,
`4 Hydrogen High`). For Neon, `4 Neon` (low) and `4 Neon Medium` (medium) were observed, while `neon high`
has not been verified yet, so for Neon only the model name is checked. Other models, image and video are
never checked: their label is only shown on stderr, so a saved file is never discarded because of one. What a
real fallback to a lightweight model looks like was never seen (it cannot be provoked without spending
the quota); when no label is found the script says so on stderr and exits 0.

## Which reference to read

- `references/limits.md`: before choosing Neon or high effort on a tight quota, before attaching large
  files or PDFs, when deciding whether Deep Research fits, and for why Tasks is not supported.
- `references/auth.md`: on exit code 2, on first use, or when the web layer changes after a
  `gemini-webapi` upgrade.
- `references/media.md`: before calling `--mode image` or `--mode video`, for prompting structure, step-by-step `--ref` edits, consistency, output inspection, and media failure handling.
