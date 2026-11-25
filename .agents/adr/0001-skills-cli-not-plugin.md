# Install through the `skills` CLI, not a plugin

Date: 2026-11-15. Status: accepted; the status field was dropped by [ADR 0002](0002-no-status-field.md).

## Context

Only stable skills should install by default; drafts and retired skills stay public but out of the way. Two ways exist to ship a curated set:

- a Claude Code plugin whose `plugin.json` lists each stable skill path;
- the `skills` CLI (`npx skills add pv-ca/skills`), which walks `skills/` up to three levels deep.

A plugin namespaces every skill under the plugin name, so `/expert` becomes `/<plugin>:expert`. The skills in this repo are mostly typed by hand, often at the end of a message, so the short name matters.

## What was tested

On 2026-11-15, with a throwaway repo holding `skills/productivity/expert`, `skills/in-progress/rascunho` and `skills/deprecated/velha`:

- `npx skills add <repo> --list` listed all three. The CLI finds bucketed skills with no manifest at all.
- A `.claude-plugin/plugin.json` with `"skills": ["./skills/productivity/expert"]` did not narrow the CLI's list.
- A `skills.sh.json` with `paths` did not narrow it either; `paths` adds places to search.
- Adding `metadata: internal: true` to the two non-promoted skills left only `expert` in `--list`, and `--all` installed only `expert`.

## Decision

Curate with `metadata.internal: true` on every skill that is not `stable`, and document `npx skills add pv-ca/skills` as the install path. Ship no plugin manifest for now. Since the CLI does not need bucket folders to curate, skills sit flat in `skills/<name>/` and their status lives in the frontmatter.

## Consequences

- Skills keep their short names (`/expert`).
- Users update with `npx skills update`; nothing updates by itself.
- `scripts/check.sh` must enforce the `internal` flag, since forgetting it ships a draft.
- Revisit if users ask for an auto-updating install: a plugin can be added later beside this layout without moving any skill.
