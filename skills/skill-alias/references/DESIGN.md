# skill-alias — Design Reference

## Concept

A single skill that acts as an alias manager for all other skills.
Users install this once, then create short slash commands instead of remembering long skill names and paths.

Analogy: like `alias` in bash shell, but for AI agent skills.

## Config location

All config lives in `~/.skill-alias/mappings.yaml`

```yaml
mappings:
  - alias: /review
    skill: code-review
    path: /mnt/skills/plugins/engineering:code-review/SKILL.md
  - alias: /test
    skill: testing-strategy
    path: /mnt/skills/plugins/engineering:testing-strategy/SKILL.md
```

## Command flows

### create
1. Validate path exists and contains valid SKILL.md
2. Normalize alias (ensure starts with `/`)
3. Check for conflicts → ask user to confirm overwrite if alias exists
4. Append to mappings.yaml (create file + directory if not exists)
5. Confirm success

### list
1. Read mappings.yaml
2. For each mapping, check if path still exists
3. Display table with status: ✅ OK or ❌ MISS

### remove
1. Find alias in mappings.yaml
2. Confirm with user before removing
3. Remove entry and save

### init [path]
1. Scan given path (default: known skill directories for current framework)
2. For each SKILL.md found, read `name` and `description` from frontmatter
3. Suggest short aliases based on name keywords
4. Present mapping table to user for confirmation
5. Save confirmed mappings to mappings.yaml

### resolve (internal — called when user types any /command)
1. Read mappings.yaml
2. Find matching alias
3. Return path of mapped SKILL.md
4. If not found: exit with error

## Alias resolution flow

```
User types /review PR#123
       ↓
skill-alias reads mappings.yaml
       ↓
Finds: /review → code-review → /path/to/SKILL.md
       ↓
AI reads that SKILL.md and executes as if invoked directly
       ↓
Passes "PR#123" as argument to the target skill
```

## Supported frameworks

- Claude Code
- Cowork (any agent that reads SKILL.md)
- Planned: Codex, Copilot

## Path handling

- Config dir: `~/.skill-alias/` (cross-platform via `Path.home()`)
- Scripts use `Path(__file__).parent` to locate sibling files — never relies on cwd
