#!/usr/bin/env python3
"""
Usage: python resolve.py <alias>
Resolves an alias to its SKILL.md path. Prints the path to stdout.
Exit code 0 = found, 1 = not found.
"""

import sys
import yaml
from pathlib import Path

MAPPINGS_FILE = Path.home() / ".skill-alias" / "mappings.yaml"


def main():
    if len(sys.argv) < 2:
        print("Usage: resolve.py <alias>")
        sys.exit(1)

    alias = sys.argv[1]
    if not alias.startswith("/"):
        alias = "/" + alias

    if not MAPPINGS_FILE.exists():
        sys.exit(1)

    with open(MAPPINGS_FILE) as f:
        data = yaml.safe_load(f) or {}

    mappings = data.get("mappings") or []
    match = next((m for m in mappings if m["alias"] == alias), None)

    if not match:
        sys.exit(1)

    path = Path(match["path"]).expanduser()
    if not path.exists():
        print(f"❌ Mapped path not found: {match['path']}", file=sys.stderr)
        sys.exit(1)

    print(str(path))


if __name__ == "__main__":
    main()
