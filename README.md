# skill-alias

One skill to manage all your skills. Install once, alias everything.

## What is this?

A single skill you install into your agent (Claude Code, Cowork, etc.) that lets you:

- **Create short aliases** for any skill: `/review` instead of `engineering:code-review`
- **Auto-discover** all installed skills and suggest aliases
- **Route** slash commands to the right skill automatically

## Install

Copy the `skill-alias` folder into your agent's skill directory:

```bash
# Claude Code
cp -r skill-alias /mnt/skills/user/skill-alias

# Or wherever your agent loads skills from
```

That's it. One install, done forever.

## Usage

```
# Auto-discover all skills and create aliases
/skill-alias init

# Manually create an alias
/skill-alias create /review code-review /mnt/skills/plugins/engineering:code-review/SKILL.md

# See all aliases
/skill-alias list

# Remove an alias
/skill-alias remove /review

# Use an alias — just type it
/review PR#123
/test src/utils.js
/debug "connection timeout error"
```

## How it works

1. Aliases are stored in `~/.skill-alias/mappings.yaml`
2. When you type `/review`, the agent reads the mapping file
3. Finds `/review → code-review → /path/to/SKILL.md`
4. Loads that skill and executes it as if you called it directly
5. No duplication, no copy, always uses the original skill file

## Config format

```yaml
# ~/.skill-alias/mappings.yaml
mappings:
  - alias: /review
    skill: code-review
    path: /mnt/skills/plugins/engineering:code-review/SKILL.md
  - alias: /test
    skill: testing-strategy
    path: /mnt/skills/plugins/engineering:testing-strategy/SKILL.md
```

## Supported frameworks

- **Now:** Claude Code, Cowork (any agent that reads SKILL.md)
- **Planned:** Codex, Copilot

## License

MIT
