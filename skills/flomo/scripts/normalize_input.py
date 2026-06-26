#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from pypdf import PdfReader  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    PdfReader = None

TEXT_ENCODINGS = ["utf-8-sig", "utf-8", "gb18030", "gbk", "big5", "latin-1"]
LOCAL_TZ = timezone(timedelta(hours=8))
DATE_LINE_RE = re.compile(r"^\s*(?:\[date\]\s*)?(\d{4}-\d{2}-\d{2})(?:[ T](\d{2}:\d{2}(?::\d{2})?)?)?\s*$", re.I)


def read_text_file(path: Path) -> str:
    data = path.read_bytes()
    for encoding in TEXT_ENCODINGS:
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def extract_pdf_text(path: Path) -> str:
    if PdfReader is None:
        raise RuntimeError("pypdf is not installed; install pypdf or add a PDF text extraction backend")
    reader = PdfReader(str(path))
    parts: list[str] = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts)


def read_source(path: Path | None, text: str | None) -> tuple[str, str]:
    if text is not None:
        return text, "pasted"
    if path is None:
        raise ValueError("either path or text must be provided")
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf_text(path), "pdf"
    if suffix in {".txt", ".md", ".markdown", ".rst"}:
        return read_text_file(path), suffix.lstrip(".")
    raise ValueError(f"Unsupported file type: {path.suffix}")


def parse_local_datetime(value: str) -> datetime | None:
    raw = value.strip().replace("T", " ")
    formats = [
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(raw, fmt)
        except ValueError:
            continue
        return dt.replace(tzinfo=LOCAL_TZ)
    return None


def format_local_datetime(dt: datetime) -> str:
    return dt.astimezone(LOCAL_TZ).isoformat(timespec="seconds")


def normalize_created_at(date_part: str, time_part: str | None) -> str:
    raw = date_part if not time_part else f"{date_part} {time_part}"
    dt = parse_local_datetime(raw)
    if dt is None:
        raise ValueError(f"Unable to parse date: {raw}")
    return format_local_datetime(dt)


def split_blocks(text: str) -> list[str]:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    blocks: list[str] = []
    current: list[str] = []
    for line in lines:
        if not line.strip():
            if current:
                blocks.append("\n".join(current).strip())
                current = []
            continue
        current.append(line)
    if current:
        blocks.append("\n".join(current).strip())
    return blocks


def parse_generic_blocks(text: str, source_type: str, source_path: str | None) -> dict:
    blocks = split_blocks(text)
    notes: list[dict] = []
    pending_date: str | None = None

    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if not lines:
            continue

        m = DATE_LINE_RE.match(lines[0])
        if m and len(lines) == 1:
            pending_date = normalize_created_at(m.group(1), m.group(2))
            continue

        created_at: str | None = None
        content_lines = lines
        if m:
            created_at = normalize_created_at(m.group(1), m.group(2))
            content_lines = lines[1:]
        elif pending_date:
            created_at = pending_date
            pending_date = None

        content = "\n".join(content_lines).strip()
        if not content:
            continue
        notes.append(
            {
                "content": content,
                "created_at": created_at,
                "tag": None,
                "chapter": None,
                "book_title": None,
                "author": None,
                "reading_started_at": None,
                "reading_ended_at": None,
                "source_path": source_path,
                "source_type": source_type,
                "source_format": "generic_blocks",
            }
        )

    return {
        "source_path": source_path,
        "source_type": source_type,
        "source_format": "generic_blocks",
        "note_count": len(notes),
        "notes": notes,
    }


def parse_input(text: str, source_type: str, source_path: str | None) -> dict:
    return parse_generic_blocks(text, source_type, source_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize pasted text or files into memo blocks")
    parser.add_argument("path", nargs="?", help="Source file path")
    parser.add_argument("--text", help="Raw pasted text")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of raw text")
    args = parser.parse_args()

    path = Path(args.path) if args.path else None
    raw, source_type = read_source(path, args.text)
    payload = parse_input(raw, source_type, str(path) if path else None)

    if args.json:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        for note in payload["notes"]:
            sys.stdout.write(note["content"])
            sys.stdout.write("\n---\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
