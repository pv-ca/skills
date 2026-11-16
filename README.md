<h1 align="center">pv-ca/skills</h1>

<p align="center">Skills I made and use every day. Take what helps you.</p>

<p align="center"><a href="LICENSE"><img src="https://img.shields.io/github/license/pv-ca/skills?style=flat" alt="License"></a> <a href="https://github.com/pv-ca/skills/actions/workflows/check.yml"><img src="https://github.com/pv-ca/skills/actions/workflows/check.yml/badge.svg" alt="check"></a></p>

## Install

Paste into your coding agent:

```text
Install the skills from https://github.com/pv-ca/skills, following the Install section of its README.
```

Or run it yourself. It works with any agent the [`skills` CLI](https://github.com/vercel-labs/skills) supports, needs Node.js, and asks which agents and skills you want:

```bash
npx skills add pv-ca/skills
```

- **One skill:** `npx skills add pv-ca/skills --skill expert`.
- **Update:** `npx skills update`.
- **For your user instead of the current project:** add `-g`.

Claude Code without Node.js:

```bash
git clone https://github.com/pv-ca/skills ~/src/pv-ca-skills && ~/src/pv-ca-skills/scripts/link-skills.sh
```

Skills are installed under their own names, so you type `/expert`, not `/<plugin>:expert`.

## Skills

### Planning and prompts

- **[expert](skills/expert/)**: add `/expert` to a task and get it back the way a top professional in its field would ask for it. Deeper, not bigger. [Example](skills/expert/example.md).

## What every skill here has

| | Why |
| --- | --- |
| `SKILL.md` | The instructions the agent reads. |
| `README.md` | For you: what it does, when to reach for it, an example, and how to tell it worked. |
| `example.md` | A real, unedited output, so you see what you get before installing. |
| `evals.json` | Cases that must fire the skill and cases that must not, each with what a good reply looks like. `scripts/eval.py <skill>` runs them in fresh `claude -p` sessions. |

Every push runs `scripts/check.py`, which fails if a skill breaks a rule in [AGENTS.md](AGENTS.md): a stable skill without tests or docs, a draft that would install by default, a skill name used twice.

## Drafts

Skills marked `in-progress` are public but not installed by default. To try one: `INSTALL_INTERNAL_SKILLS=1 npx skills add pv-ca/skills --skill <name>`.

## Contributing

Open an issue with what you typed, what the skill did, and what you expected. A failure seen in a real session is the most useful report there is.

## License

[MIT](LICENSE).
