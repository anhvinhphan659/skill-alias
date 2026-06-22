---
name: skill-alias
description: >
  Centralized skill alias manager. Use this skill when the user types any command starting with /skill-alias
  (e.g., /skill-alias create, /skill-alias list, /skill-alias remove, /skill-alias init).
  Also use this skill when the user types ANY slash command — first run resolve.py to check if it's a known alias,
  then load and execute the mapped skill if found.
---

# skill-alias

Manage short slash command aliases that map to installed skills.
All scripts are in `scripts/` relative to this file. Requires Python 3 and `pyyaml`.

## Commands

### /skill-alias create \<alias\> \<skill-name\> \<path-to-SKILL.md\>

```
python scripts/create.py <alias> <skill-name> <path-to-SKILL.md>
```

Add `--force` to overwrite an existing alias without prompting.

### /skill-alias list

```
python scripts/list.py
```

### /skill-alias remove \<alias\>

```
python scripts/remove.py <alias>
```

Script will prompt user to confirm. Pass the confirmation through.

### /skill-alias init [\<scan-path\>]

```
python scripts/init.py [scan-path]
```

Script outputs proposed mappings as JSON. Present the table to the user, ask for confirmation,
then for each confirmed mapping run `scripts/create.py` to save it.

## Resolving aliases (when user types any /command)

When the user types a `/command` that is not a built-in:

1. Run: `python scripts/resolve.py <command>`
2. If exit code 0: read the SKILL.md path printed to stdout, load it, execute as if invoked directly. Pass any arguments after the command to the target skill.
3. If exit code 1: tell user the alias doesn't exist, suggest `/skill-alias list` or `/skill-alias init`.

## First-time setup

If `~/.skill-alias/mappings.yaml` doesn't exist, the scripts create it automatically.
Suggest the user runs `/skill-alias init` to get started.
