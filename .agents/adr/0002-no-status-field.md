# No status field in the frontmatter

Date: 2026-11-25. Status: accepted. Replaces the status part of [ADR 0001](0001-skills-cli-not-plugin.md).

## Context

Each `SKILL.md` carried `metadata.status` (`stable`, `in-progress`, `deprecated`). Only this repository's scripts read it. The Agent Skills specification makes `metadata` optional, and the `skills` CLI hides a skill by `metadata.internal` alone.

## What was checked

On 2026-11-25, the frontmatter of 254 `SKILL.md` files on the default branch of 10 public repositories (`anthropics/skills`, `mattpocock/skills`, `obra/superpowers`, `vercel-labs/agent-skills`, `vercel-labs/skills`, `openai/skills`, `supabase/agent-skills`, `trailofbits/skills`, `antfu/skills`, `kepano/obsidian-skills`): none had a `status` or `internal` key; 34 had `metadata`.

## Decision

Drop `metadata.status`. A skill is published unless it sets `metadata.internal: true`. A retired skill is deleted.

## Consequences

- A published skill's frontmatter needs only `name` and `description`.
- A skill without `internal` must meet every published-skill rule in `scripts/check.py`.
- `scripts/link-skills.sh` reads no frontmatter and links every skill folder. Deleting a skill leaves its old link dangling on machines that ran it.
