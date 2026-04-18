#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from flomo_common import normalize_text


def load_notes(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8", errors="replace").strip()
    if not raw:
        return []
    if raw.startswith("[") or raw.startswith("{"):
        data = json.loads(raw)
        if isinstance(data, dict) and "notes" in data and isinstance(data["notes"], list):
            return [item for item in data["notes"] if isinstance(item, dict)]
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
        raise ValueError("JSON input must be a list or an object with a notes array")
    notes: list[dict] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        item = json.loads(line)
        if isinstance(item, dict):
            notes.append(item)
    return notes


def main() -> int:
    parser = argparse.ArgumentParser(description="Find exact duplicate notes after normalization")
    parser.add_argument("path", help="JSON or JSONL file with note objects")
    parser.add_argument("--field", default="content", help="Field used for duplicate detection")
    parser.add_argument("--show-normalized", action="store_true", help="Include normalized text in the output")
    args = parser.parse_args()

    notes = load_notes(Path(args.path))
    groups: dict[str, list[dict]] = defaultdict(list)
    for note in notes:
        content = str(note.get(args.field, ""))
        key = normalize_text(content)
        groups[key].append(note)

    duplicates = []
    for normalized, group in groups.items():
        if len(group) < 2:
            continue
        record = {
            "count": len(group),
            "notes": group,
        }
        if args.show_normalized:
            record["normalized"] = normalized
        duplicates.append(record)

    json.dump(
        {
            "duplicate_groups": duplicates,
            "duplicate_count": len(duplicates),
            "total_notes": len(notes),
        },
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
