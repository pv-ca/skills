#!/usr/bin/env bash
# Link every skill except deprecated ones into ~/.claude/skills, so `git pull` keeps them current.
# Refuses to replace anything that is not already a link into this repository.
set -euo pipefail
repo=$(cd "$(dirname "$0")/.." && pwd -P)
dest=${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}
mkdir -p "$dest"
for skill in "$repo"/skills/*/; do
  skill=${skill%/}
  name=${skill##*/}
  [[ -f $skill/SKILL.md ]] || { echo "skip $name: no SKILL.md" >&2; continue; }
  # status is read from the frontmatter only (between the first two --- lines)
  status=$(awk 'NR==1 && $0!="---"{exit} NR>1 && $0=="---"{exit} NR>1 && $1=="status:"{gsub(/["\047]/,"",$2); print $2}' "$skill/SKILL.md")
  [[ $status == deprecated ]] && continue
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
