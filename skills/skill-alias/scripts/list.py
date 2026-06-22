#!/usr/bin/env python3
"""
Usage: python list.py
Lists all alias mappings with status check.
"""

import yaml
from pathlib import Path

CONFIG_DIR = Path.home() / ".skill-alias"
MAPPINGS_FILE = CONFIG_DIR / "mappings.yaml"


def main():
    if not MAPPINGS_FILE.exists():
        print("No mappings found. Run: /skill-alias init")
        return

    with open(MAPPINGS_FILE) as f:
        data = yaml.safe_load(f) or {}

    mappings = data.get("mappings") or []

    if not mappings:
        print("No aliases defined. Run: /skill-alias init")
        return

    col_alias = max(len(m["alias"]) for m in mappings)
    col_skill = max(len(m["skill"]) for m in mappings)
    col_alias = max(col_alias, 5)
    col_skill = max(col_skill, 5)

    header = f"{'Alias':<{col_alias}}  {'Skill':<{col_skill}}  {'Path':<50}  Status"
    print(header)
    print("-" * len(header))

    for m in mappings:
        path = Path(m["path"]).expanduser()
        status = "✅ OK" if path.exists() else "❌ MISS"
        path_str = m["path"]
        if len(path_str) > 50:
            path_str = "..." + path_str[-47:]
        print(f"{m['alias']:<{col_alias}}  {m['skill']:<{col_skill}}  {path_str:<50}  {status}")


if __name__ == "__main__":
    main()
