#!/usr/bin/env python3
"""
Usage: python init.py [scan-path]
Auto-discovers SKILL.md files, suggests aliases, prints proposed mappings as JSON.
The AI agent handles user confirmation before saving.
"""

import sys
import json
import re
import yaml
from pathlib import Path

CONFIG_DIR = Path.home() / ".skill-alias"
MAPPINGS_FILE = CONFIG_DIR / "mappings.yaml"

# Default scan paths per common frameworks
DEFAULT_SCAN_PATHS = [
    Path.home() / ".claude" / "skills",
    Path("/mnt/skills/user"),
    Path("/mnt/skills/plugins"),
    Path.home() / ".cowork" / "skills",
]


def read_frontmatter(skill_file: Path) -> dict:
    try:
        content = skill_file.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return {}
        end = content.index("---", 3)
        fm = yaml.safe_load(content[3:end])
        return fm or {}
    except Exception:
        return {}


def suggest_alias(name: str) -> str:
    # Take first meaningful word, lowercase, strip special chars
    words = re.split(r"[\s\-_:]+", name.lower())
    words = [w for w in words if w and len(w) > 1]
    if not words:
        return "/" + re.sub(r"[^a-z0-9]", "", name.lower())[:10]
    # Prefer first word unless it's too generic
    generic = {"the", "a", "an", "my", "new", "run", "use", "get"}
    chosen = next((w for w in words if w not in generic), words[0])
    return "/" + chosen[:12]


def scan(scan_path: Path) -> list:
    results = []
    if not scan_path.exists():
        return results
    for skill_md in scan_path.rglob("SKILL.md"):
        fm = read_frontmatter(skill_md)
        name = fm.get("name") or skill_md.parent.name
        description = fm.get("description", "")
        alias = suggest_alias(name)
        results.append({
            "alias": alias,
            "skill": name,
            "path": str(skill_md),
            "description": description,
        })
    return results


def main():
    scan_path = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else None

    paths_to_scan = [scan_path] if scan_path else DEFAULT_SCAN_PATHS

    found = []
    for p in paths_to_scan:
        found.extend(scan(p))

    # Deduplicate by path
    seen_paths = set()
    unique = []
    for item in found:
        if item["path"] not in seen_paths:
            seen_paths.add(item["path"])
            unique.append(item)

    # Group by suggested alias to detect conflicts
    alias_groups: dict[str, list] = {}
    for item in unique:
        alias_groups.setdefault(item["alias"], []).append(item)

    resolved = []
    conflicts = []
    for alias, group in alias_groups.items():
        if len(group) == 1:
            resolved.append(group[0])
        else:
            conflicts.append({"alias": alias, "candidates": group})

    output = {
        "resolved": resolved,
        "conflicts": conflicts,
    }

    # Print as JSON for AI to present to user and handle conflict resolution
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
