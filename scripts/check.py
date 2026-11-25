#!/usr/bin/env python3
"""Check the repository rules in AGENTS.md. Usage: check.py [repo-root]. Exit 1 on any violation."""
import json
import re
import sys
from pathlib import Path

DOC_SECTIONS = ("## What it does", "## When to reach for it", "## It's working if")
TEXT_SUFFIXES = {".md", ".json", ".py", ".sh", ".yml", ".yaml", ".txt"}
SKIP_DIRS = {".git", ".eval-runs", "__pycache__", "node_modules"}  # generated or ignored, not repo prose


def frontmatter(text):
    """Return the top-level and metadata keys of a SKILL.md frontmatter (flat scalars only)."""
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return None
    top, meta, section = {}, {}, None
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        key = re.match(r"^(\s*)([A-Za-z_-]+):\s*(.*)$", line)
        if not key:
            continue  # continuation line of a folded value
        indent, name, value = key.groups()
        value = value.strip().strip("'\"")
        if not indent:
            section = name
            top[name] = value
        elif section == "metadata":
            meta[name] = value
    return top, meta


def check(root):
    root = Path(root)
    errors = []
    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").exists() else ""
    names = {}
    for skill_md in sorted(root.glob("skills/*/SKILL.md")):
        folder = skill_md.parent
        where = folder.relative_to(root)
        text = skill_md.read_text(encoding="utf-8")
        fm = frontmatter(text)
        if fm is None:
            errors.append(f"{where}: SKILL.md has no frontmatter")
            continue
        top, meta = fm
        name = top.get("name", "")
        if name != folder.name:
            errors.append(f"{where}: frontmatter name '{name}' differs from folder name")
        names.setdefault(name, []).append(str(where))
        if not top.get("description"):  # a folded value (">") counts as present
            errors.append(f"{where}: no description")
        if len(text.splitlines()) >= 500:
            errors.append(f"{where}: SKILL.md has 500 lines or more")
        internal = meta.get("internal", "").lower() in ("true", "1")
        linked = f"skills/{folder.name}/" in readme
        if internal:
            if linked:
                errors.append(f"{where}: an internal skill must not be linked from README.md")
        else:
            if not linked:
                errors.append(f"{where}: published skill not linked from README.md as skills/{folder.name}/")
            yaml_path = folder / "agents" / "openai.yaml"
            yaml_text = yaml_path.read_text(encoding="utf-8") if yaml_path.exists() else ""
            for key in ("display_name", "short_description"):
                if not re.search(rf"^\s+{key}:\s*\S", yaml_text, re.M):
                    errors.append(f"{where}: agents/openai.yaml lacks interface.{key}")
            doc = folder / "README.md"
            doc_text = doc.read_text(encoding="utf-8") if doc.exists() else ""
            for section in DOC_SECTIONS:
                if section not in doc_text:
                    errors.append(f"{where}: README.md lacks '{section}'")
            errors += check_evals(folder, where)
    for name, places in names.items():
        if len(places) > 1:
            errors.append(f"skill name '{name}' used more than once: {places}")
    for path in sorted(root.rglob("*")):
        if not path.is_file() or SKIP_DIRS & set(path.parts) or path.suffix not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8", errors="replace")
        for n, line in enumerate(text.splitlines(), 1):
            if "\u2014" in line:
                errors.append(f"{rel}:{n}: em dash")
            if rel.parts[0] == "skills" and re.search(r"/home/|/Users/|C:\\Users\\", line):
                errors.append(f"{rel}:{n}: absolute home path")
    return errors


def check_evals(folder, where):
    path = folder / "evals.json"
    try:
        cases = json.loads(path.read_text(encoding="utf-8"))["cases"]
    except (OSError, ValueError, KeyError, TypeError) as e:
        return [f"{where}: evals.json missing or invalid ({e.__class__.__name__})"]
    errors, expects, ids = [], set(), set()
    for i, case in enumerate(cases if isinstance(cases, list) else []):
        if not isinstance(case, dict) or not all(isinstance(case.get(k), str) and case[k] for k in ("id", "message", "expect", "judge")):
            errors.append(f"{where}: evals.json case {i} needs non-empty id, message, expect, judge")
            continue
        if case["expect"] not in ("fires", "silent"):
            errors.append(f"{where}: evals.json case '{case['id']}' expect must be fires or silent")
        if case["id"] in ids:
            errors.append(f"{where}: evals.json case id '{case['id']}' repeated")
        ids.add(case["id"])
        expects.add(case["expect"])
    if not {"fires", "silent"} <= expects:
        errors.append(f"{where}: evals.json needs at least one 'fires' and one 'silent' case")
    return errors


if __name__ == "__main__":
    problems = check(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)
    for p in problems:
        print(p)
    print(f"{len(problems)} problem(s)" if problems else "ok")
    sys.exit(1 if problems else 0)
