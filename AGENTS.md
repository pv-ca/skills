# Maintaining this repository

Rules for adding or changing a skill. `scripts/check.py` enforces every rule marked (checked). CI runs it, and its tests, on each push. Run `python3 scripts/check.py` before committing.

## Layout

One folder per skill, flat: `skills/<name>/`. The folder name equals the frontmatter `name` (checked). Names are unique (checked).

A skill's status lives in its frontmatter, not in its path, so changing status never breaks a link:

```yaml
metadata:
  status: stable        # stable | in-progress | deprecated (checked)
  internal: true        # required unless stable (checked); hides it from `npx skills add`
```

`metadata.internal` is how the `skills` CLI hides a skill (see [ADR 0001](.agents/adr/0001-skills-cli-not-plugin.md) for the test). Forgetting it ships a draft, which is why it is checked.

## A stable skill has

- `SKILL.md`, under 500 lines (checked). Detail the agent reads only sometimes goes in files beside it.
- `README.md` with the sections `## What it does`, `## When to reach for it`, `## It's working if` (checked), plus an `## Example` that quotes `example.md`.
- `example.md`: one real output, unedited, with the input that produced it. Never write an example by hand.
- `evals.json`: at least one `fires` case and one `silent` case, each with `id`, `message`, `expect` and `judge` (checked). Messages are neutral: no personal data, no private projects.
- `agents/openai.yaml` with `interface.display_name` and `interface.short_description`, for the Codex picker (checked).
- A link from the top-level `README.md` as `skills/<name>/` (checked), under a heading that says what kind of work it serves.

A draft or deprecated skill needs only `SKILL.md`, and must not be linked from the top-level `README.md` (checked).

## Writing a skill

- Model-invoked is the default: the description says what it does and what should fire it. A skill that only a person should start sets `disable-model-invocation: true` in the frontmatter and `policy: { allow_implicit_invocation: false }` in `agents/openai.yaml`, and its description is one plain line.
- A skill that a person types in the middle of a message must stay model-invoked, or the model will not recognise the tag.
- To use another skill, say to call the Skill tool with its name, one call per skill. Never link into another skill's folder.
- A skill that starts a subagent says to start it with a fresh context.
- Nothing may depend on the maintainer's machine, accounts or private projects (absolute home paths are checked).
- No em dashes in any file (checked). Rewrite the sentence; never swap the character blindly.

## Changing a skill

1. Run its evals before the change: `python3 scripts/eval.py <name>`. Note the result.
2. Change it.
3. Run the evals again and judge each `result.md` against its `judge` line. A case that passed before and fails now blocks the change.
4. If the output changed in a way a user would see, regenerate `example.md` from a real run.
5. Add a line under `## Unreleased` in `CHANGELOG.md`, with the eval result.

## Status changes

- Promote (`in-progress` to `stable`): remove `internal`, add the files a stable skill has, link it from the README.
- Retire (to `deprecated`): add `internal: true`, remove its README link, say in its own `README.md` what replaces it.

## Releases

A release moves the `## Unreleased` lines under a version heading and tags `vX.Y.Z`: minor for a new or changed skill, patch for fixes, major when a skill is removed or renamed.

## Local install

`scripts/link-skills.sh` links every non-deprecated skill into `~/.claude/skills/` (or `$CLAUDE_SKILLS_DIR`). It refuses to replace anything that is not already a link into this repository.
