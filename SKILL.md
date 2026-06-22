---
name: skill-alias
description: >
  Centralized skill alias manager. Use this skill when the user types any command starting with /skill-alias
  (e.g., /skill-alias init, /skill-alias add, /skill-alias list, /skill-alias remove).
  Also use this skill when the user types ANY slash command — first run resolve.py to check if it's a known alias,
  then load and execute the mapped skill if found.
---

# skill-alias

Manage short slash command aliases that map to installed skills.
All scripts are in `scripts/` relative to this file. Requires Python 3 and `pyyaml`.

## Commands

### /skill-alias init [\<scan-path\>]

```
python scripts/init.py [scan-path]
```

Script outputs JSON with two keys:
- `resolved`: list of proposed mappings with no alias conflict
- `conflicts`: list of aliases where multiple skills matched — each has `alias` and `candidates` array

Steps:
1. Present `resolved` mappings as a table for user to confirm
2. For each item in `conflicts`: show candidates numbered, ask user to pick one (or skip)
3. After user confirms, run `scripts/add.py` for each accepted mapping

### /skill-alias add \<alias\> \<skill-name\> \<path-to-SKILL.md\>

```
python scripts/add.py <alias> <skill-name> <path-to-SKILL.md>
```

If alias already exists, script will prompt to confirm overwrite. Pass the prompt through to user.

### /skill-alias list

```
python scripts/list.py
```

### /skill-alias remove \<alias\>

```
python scripts/remove.py <alias>
```

Script will prompt user to confirm. Pass the confirmation through.

## Alias resolution (internal — triggered by any unrecognized /command)

When the user types a `/command` that is not a built-in skill-alias command:

1. Run: `python scripts/resolve.py <command>`
2. Exit code 0: read the SKILL.md path printed to stdout → load it → execute as if invoked directly, passing any arguments after the command to the target skill
3. Exit code 1: tell user the alias doesn't exist, suggest `/skill-alias list` or `/skill-alias init`

## First-time setup

If `~/.skill-alias/mappings.yaml` doesn't exist, the scripts create it automatically.
Suggest the user runs `/skill-alias init` to get started.
