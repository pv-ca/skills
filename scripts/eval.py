#!/usr/bin/env python3
"""Run a skill's evals.json cases in fresh, top-level `claude -p` sessions.

Usage: eval.py <skill> [--model sonnet] [--case <id>] [--out .eval-runs]

Each case runs in its own empty folder. The skill is copied there as the project skill
`<skill>-eval` and the message's `/<skill>` becomes `/<skill>-eval`, because a personal skill
with the same name would win over the project copy. A `fires` case passes when the skill is
called and no file is edited; a `silent` case passes when it is not called. The reply is saved
as result.md next to the case's `judge` text, for a person to judge the quality.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDIT_TOOLS = {"Edit", "Write", "NotebookEdit"}
# Run as a top-level session, not as a child of the session that called this script.
NESTING_VARS = ("CLAUDECODE", "CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_ENTRYPOINT")


def install_copy(skill_dir, work, alias):
    dst = work / ".claude" / "skills" / alias
    shutil.copytree(skill_dir, dst)
    md = dst / "SKILL.md"
    text = md.read_text(encoding="utf-8")
    new, n = re.subn(r"^name:[ \t]*['\"]?[^\s'\"]+['\"]?[ \t]*\r?$", f"name: {alias}", text, count=1, flags=re.M)
    if n != 1:
        raise SystemExit(f"{md}: no 'name:' line to rewrite")
    md.write_text(new, encoding="utf-8")


def alias_message(message, skill, alias):
    return re.sub(rf"(^|\s)/{re.escape(skill)}(?=$|\s|[.,;:!?])", rf"\1/{alias}", message)


def snapshot(work):
    """Paths and mtimes of the files in the case folder, to catch edits made by any tool."""
    return {p: p.stat().st_mtime_ns for p in work.rglob("*") if p.is_file() and p.name not in ("run.jsonl", "result.md")}


def parse(raw, alias=None, message=""):
    """Return (skills called, edit count, final reply, is_error) from stream-json output.

    A message that starts with `/<alias>` is expanded by the CLI itself, with no Skill tool
    call; it counts as called when the session's init event lists the alias as loaded.
    """
    skills, edits, result, is_error = [], 0, "", False
    slash = alias is not None and re.match(rf"\s*/{re.escape(alias)}(?=$|\s)", message)
    for line in raw.splitlines():
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if not isinstance(d, dict):
            continue
        if slash and d.get("type") == "system" and d.get("subtype") == "init":
            if alias in (d.get("skills") or []) or alias in (d.get("slash_commands") or []):
                skills.append(alias)
        if d.get("type") == "result":
            result = d.get("result") if isinstance(d.get("result"), str) else ""
            is_error = bool(d.get("is_error"))
        msg = d.get("message")
        content = msg.get("content") if isinstance(msg, dict) else None
        for c in content if isinstance(content, list) else []:
            if isinstance(c, dict) and c.get("type") == "tool_use":
                inp = c.get("input")
                if c.get("name") == "Skill" and isinstance(inp, dict):
                    skills.append(inp.get("skill"))
                if c.get("name") in EDIT_TOOLS:
                    edits += 1
    return skills, edits, result, is_error


def verdict(case, alias, skills, edits, result, is_error, returncode=0):
    if is_error or not result or returncode != 0:
        return "ERROR"
    called = alias in skills
    if case["expect"] == "fires":
        return "pass" if called and edits == 0 else "FAIL"
    return "pass" if not called else "FAIL"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skill")
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--case")
    ap.add_argument("--out", default=str(ROOT / ".eval-runs"))
    args = ap.parse_args()

    skill_dir = ROOT / "skills" / args.skill
    cases = json.loads((skill_dir / "evals.json").read_text(encoding="utf-8"))["cases"]
    if args.case:
        cases = [c for c in cases if c["id"] == args.case]
        if not cases:
            raise SystemExit(f"no case '{args.case}'")
    alias = f"{args.skill}-eval"
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if k not in NESTING_VARS}

    failed = 0
    for case in cases:
        work = Path(tempfile.mkdtemp(prefix=f"{args.skill}-{case['id']}-", dir=out))
        install_copy(skill_dir, work, alias)
        message = alias_message(case["message"], args.skill, alias)
        before = snapshot(work)
        proc = subprocess.run(
            ["claude", "-p", "--model", args.model, "--output-format", "stream-json", "--verbose", message],
            cwd=work, env=env, capture_output=True, text=True,
        )
        raw = proc.stdout + proc.stderr
        (work / "run.jsonl").write_text(raw, encoding="utf-8")
        skills, edits, result, is_error = parse(raw, alias, message)
        if snapshot(work) != before:
            edits += 1  # a file changed through Bash, a subagent or any other tool
        (work / "result.md").write_text(f"<!-- judge: {case['judge']} -->\n\n{result}", encoding="utf-8")
        if "Not logged in" in raw and not result:
            raise SystemExit("claude CLI is not logged in: run `claude` and /login first")
        v = verdict(case, alias, skills, edits, result, is_error, proc.returncode)
        failed += v != "pass"
        print(f"{v:5} {case['id']:28} expect={case['expect']:6} skills={skills or '-'} edits={edits} exit={proc.returncode} -> {work / 'result.md'}")
    print(f"{len(cases) - failed}/{len(cases)} passed. Judge each result.md against its judge line.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
