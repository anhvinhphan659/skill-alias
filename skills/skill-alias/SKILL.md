---
name: skill-alias
description: >
  Centralized skill alias manager. Use this skill when the user types any command starting with /skill-alias
  (e.g., /skill-alias create, /skill-alias list, /skill-alias remove, /skill-alias init).
  Also use this skill when the user types ANY slash command that matches an alias defined in ~/.skill-alias/mappings.yaml
  — read that file first to check if the alias exists, then load and execute the mapped skill.
---

# skill-alias

You are a skill router. Your job is to manage and resolve skill aliases so users can type short slash commands
instead of remembering long skill names and paths.

## Config location

All config lives in `~/.skill-alias/mappings.yaml`

Format:
```yaml
mappings:
  - alias: /review
    skill: code-review
    path: /mnt/skills/plugins/engineering:code-review/SKILL.md
  - alias: /test
    skill: testing-strategy
    path: /mnt/skills/plugins/engineering:testing-strategy/SKILL.md
```

## Commands

### /skill-alias create <alias> <skill-name> <path-to-SKILL.md>

Create a new alias mapping.

Steps:
1. Validate that the path exists and contains a valid SKILL.md
2. Normalize alias (ensure starts with `/`)
3. Check `~/.skill-alias/mappings.yaml` for conflicts — if alias exists, ask user to confirm overwrite
4. Append to mappings.yaml (create file + directory if not exists)
5. Confirm: `✅ Created: /review → code-review (/mnt/skills/plugins/engineering:code-review/SKILL.md)`

### /skill-alias list

Show all current mappings in a table:
```
Alias           Skill                    Path                                         Status
/review         code-review              /mnt/skills/plugins/engineering:.../SKILL.md  ✅ OK
/test           testing-strategy         /mnt/skills/plugins/engineering:.../SKILL.md  ✅ OK
/debug          debug                    /mnt/skills/plugins/engineering:.../SKILL.md  ❌ MISS
```
Check each path exists → show OK or MISS.

### /skill-alias remove <alias>

Remove an alias from mappings.yaml. Confirm before removing.

### /skill-alias init [path]

Auto-discover skills:
1. Scan the given path (default: scan all known skill directories for the current framework)
2. For each SKILL.md found, read `name` and `description` from frontmatter
3. Suggest short aliases based on keywords in name/description
4. Present the full mapping table to user
5. Let user confirm, edit, or cancel
6. Save confirmed mappings to `~/.skill-alias/mappings.yaml`

### Resolving aliases (when user types a slash command like /review)

When a user types any `/command` that is NOT a built-in command:
1. Read `~/.skill-alias/mappings.yaml`
2. Find matching alias
3. If found: read the SKILL.md at the mapped path
4. Execute that skill's instructions as if the user had invoked it directly
5. If NOT found: tell user the alias doesn't exist, suggest `skill-alias list` or `skill-alias init`

**IMPORTANT**: When routing to a mapped skill, fully adopt that skill's instructions. 
You are no longer skill-alias — you ARE the target skill. Pass through any arguments the user provided after the alias.

Example: User types `/review PR#123` → resolve /review → read code-review SKILL.md → execute code review on PR#123.

## First-time setup

If `~/.skill-alias/mappings.yaml` doesn't exist when any command is run:
1. Create `~/.skill-alias/` directory
2. Create empty mappings file
3. Suggest user runs `/skill-alias init` to auto-discover skills
