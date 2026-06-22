#!/usr/bin/env python3
"""
Usage: python add.py <alias> <skill-name> <path-to-SKILL.md>
Adds a new alias mapping to ~/.skill-alias/mappings.yaml
"""

import sys
import yaml
from pathlib import Path

CONFIG_DIR = Path.home() / ".skill-alias"
MAPPINGS_FILE = CONFIG_DIR / "mappings.yaml"


def load_mappings():
    if not MAPPINGS_FILE.exists():
        return {"mappings": []}
    with open(MAPPINGS_FILE) as f:
        return yaml.safe_load(f) or {"mappings": []}


def save_mappings(data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(MAPPINGS_FILE, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


def main():
    if len(sys.argv) != 4:
        print("Usage: add.py <alias> <skill-name> <path-to-SKILL.md>")
        sys.exit(1)

    alias, skill_name, skill_path = sys.argv[1], sys.argv[2], sys.argv[3]

    # Normalize alias
    if not alias.startswith("/"):
        alias = "/" + alias

    # Validate path
    path = Path(skill_path).expanduser().resolve()
    if not path.exists():
        print(f"❌ Path not found: {skill_path}")
        sys.exit(1)
    if path.name != "SKILL.md":
        print(f"❌ Path must point to a SKILL.md file, got: {path.name}")
        sys.exit(1)

    data = load_mappings()
    mappings = data.get("mappings") or []

    # Check conflict — ask user interactively
    existing = next((m for m in mappings if m["alias"] == alias), None)
    if existing:
        print(f"⚠️  Alias {alias} already mapped to: {existing['skill']} ({existing['path']})")
        print(f"   New mapping would be:          {skill_name} ({path})")
        print("Overwrite? (y/N): ", end="", flush=True)
        answer = input().strip().lower()
        if answer != "y":
            print("Cancelled.")
            sys.exit(0)
        mappings = [m for m in mappings if m["alias"] != alias]

    mappings.append({"alias": alias, "skill": skill_name, "path": str(path)})
    data["mappings"] = mappings
    save_mappings(data)

    print(f"✅ Added: {alias} → {skill_name} ({path})")


if __name__ == "__main__":
    main()
