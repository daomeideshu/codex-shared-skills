#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Note:
    id: str | None
    created_at: datetime
    content: str
    raw: dict


def parse_datetime(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def read_notes(path: Path) -> list[dict]:
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


def coerce_notes(items: Iterable[dict]) -> list[Note]:
    notes: list[Note] = []
    for item in items:
        created_at = item.get("created_at")
        if not created_at:
            continue
        try:
            dt = parse_datetime(str(created_at))
        except Exception:
            continue
        notes.append(
            Note(
                id=str(item.get("id")) if item.get("id") is not None else None,
                created_at=dt,
                content=str(item.get("content", "")),
                raw=item,
            )
        )
    notes.sort(key=lambda n: (n.created_at, n.id or ""))
    return notes


def build_windows(notes: list[Note], limit: int) -> list[dict]:
    if not notes:
        return []
    windows: list[dict] = []
    total = len(notes)
    start = 0
    while start < total:
        end = min(start + limit, total)
        chunk = notes[start:end]
        first = chunk[0].created_at
        last = chunk[-1].created_at
        span_seconds = max((last - first).total_seconds(), 0.0)
        step_seconds = int(span_seconds / max(len(chunk) - 1, 1)) if len(chunk) > 1 else 0
        windows.append(
            {
                "index": len(windows) + 1,
                "count": len(chunk),
                "step_hint_seconds": step_seconds,
                "start_created_at": first.isoformat(),
                "end_created_at": last.isoformat(),
                "note_ids": [note.id for note in chunk if note.id],
            }
        )
        start = end
    return windows


def main() -> int:
    parser = argparse.ArgumentParser(description="Build time-based pagination windows for flomo notes")
    parser.add_argument("path", help="JSON or JSONL file with note objects")
    parser.add_argument("--limit", type=int, default=50, help="Maximum notes per window")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = parser.parse_args()

    if args.limit < 1:
        raise ValueError("--limit must be at least 1")

    notes = coerce_notes(read_notes(Path(args.path)))
    windows = build_windows(notes, args.limit)
    payload = {
        "limit": args.limit,
        "total_notes": len(notes),
        "window_count": len(windows),
        "windows": windows,
    }
    if args.json:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        for window in windows:
            sys.stdout.write(
                f"#{window['index']} count={window['count']} "
                f"start={window['start_created_at']} end={window['end_created_at']} "
                f"step_hint_seconds={window['step_hint_seconds']}\n"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
