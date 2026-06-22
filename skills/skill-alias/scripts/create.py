#!/usr/bin/env python3
"""
Usage: python create.py <alias> <skill-name> <path-to-SKILL.md>
Creates a new alias mapping in ~/.skill-alias/mappings.yaml
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
        print("Usage: create.py <alias> <skill-name> <path-to-SKILL.md>")
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

    # Check conflict
    existing = next((m for m in mappings if m["alias"] == alias), None)
    if existing:
        print(f"⚠️  Alias {alias} already exists → {existing['skill']} ({existing['path']})")
        print("Pass --force to overwrite.")
        if "--force" not in sys.argv:
            sys.exit(1)
        mappings = [m for m in mappings if m["alias"] != alias]

    mappings.append({"alias": alias, "skill": skill_name, "path": str(path)})
    data["mappings"] = mappings
    save_mappings(data)

    print(f"✅ Created: {alias} → {skill_name} ({path})")


if __name__ == "__main__":
    main()
