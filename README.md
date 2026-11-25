# Skills

These are the agent skills I made and use every day. I write them for my own work, and when one keeps earning its place, it goes here.

They're small on purpose. Read one, change what doesn't fit you, make it yours.

## The skills

- **[expert](skills/expert/)**: put `/expert` at the end of a task and you get it back the way someone really good at that job would ask for it. Deeper, not bigger. ([see an example](skills/expert/example.md))
- **[gemini-web](skills/gemini-web/)**: consult your own logged-in Gemini web session from your coding agent (text, clean files, images, short videos, and Deep Research) on a separate quota, with offline guards and temporary chats by default. ([see an example](skills/gemini-web/example.md))

Each skill comes with a real output I didn't touch, and a few tests I run before changing it.

## Install

The easiest way is to ask your agent:

```text
Install the skills from https://github.com/pv-ca/skills, following the Install section of its README.
```

Or with the [`skills` CLI](https://github.com/vercel-labs/skills), which works with most agents:

```bash
npx skills add pv-ca/skills
```

Just one: `npx skills add pv-ca/skills --skill expert`. To update: `npx skills update`.

No Node? On Claude Code:

```bash
git clone https://github.com/pv-ca/skills ~/src/pv-ca-skills && ~/src/pv-ca-skills/scripts/link-skills.sh
```

## Something wrong?

Open an issue and tell me what you typed, what the skill did, and what you expected. That's the most useful thing you can send me.

## License

[MIT](LICENSE)
