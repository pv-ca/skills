#!/usr/bin/env bash
# Link every skill, drafts included, into ~/.claude/skills, so `git pull` keeps them current.
# Refuses to replace anything that is not already a link into this repository.
set -euo pipefail
repo=$(cd "$(dirname "$0")/.." && pwd -P)
dest=${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}
mkdir -p "$dest"
for skill in "$repo"/skills/*/; do
  skill=${skill%/}
  name=${skill##*/}
  [[ -f $skill/SKILL.md ]] || { echo "skip $name: no SKILL.md" >&2; continue; }
  target="$dest/$name"
  if [[ -e $target || -L $target ]]; then
    current=$(readlink -f "$target" || true)
    if [[ ! -L $target || $current != "$repo"/* ]]; then
      echo "skip $name: $target exists and is not a link into this repo" >&2
      continue
    fi
  fi
  ln -sfn "$skill" "$target"
  echo "linked $name"
done
