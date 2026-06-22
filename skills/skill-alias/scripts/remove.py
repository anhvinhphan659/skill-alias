#!/usr/bin/env python3
"""
Usage: python remove.py <alias>
Removes an alias from ~/.skill-alias/mappings.yaml
"""

import sys
import yaml
from pathlib import Path

CONFIG_DIR = Path.home() / ".skill-alias"
MAPPINGS_FILE = CONFIG_DIR / "mappings.yaml"


def main():
    if len(sys.argv) < 2:
        print("Usage: remove.py <alias>")
        sys.exit(1)

    alias = sys.argv[1]
    if not alias.startswith("/"):
        alias = "/" + alias

    if not MAPPINGS_FILE.exists():
        print(f"❌ No mappings file found.")
        sys.exit(1)

    with open(MAPPINGS_FILE) as f:
        data = yaml.safe_load(f) or {}

    mappings = data.get("mappings") or []
    existing = next((m for m in mappings if m["alias"] == alias), None)

    if not existing:
        print(f"❌ Alias not found: {alias}")
        sys.exit(1)

    print(f"Remove {alias} → {existing['skill']} ({existing['path']})?")
    print("Confirm (y/N): ", end="", flush=True)
    answer = input().strip().lower()

    if answer != "y":
        print("Cancelled.")
        sys.exit(0)

    data["mappings"] = [m for m in mappings if m["alias"] != alias]

    with open(MAPPINGS_FILE, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    print(f"✅ Removed: {alias}")


if __name__ == "__main__":
    main()
