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
WECHAT_META_TIME_RE = re.compile(r"^\*\s*(开始时间|结束时间)：(.+?)\s*$")
WECHAT_NOTE_COUNT_RE = re.compile(r"^(\d+)\s*个笔记\s*$")
WECHAT_CHAPTER_RE = re.compile(r"^##\s+(.+?)\s*$")
WECHAT_HR_RE = re.compile(r"^<hr\s*/?>\s*$", re.I)


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


def trim_blank_edges(lines: list[str]) -> list[str]:
    start = 0
    end = len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]


def split_wechat_blocks(lines: list[str]) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if WECHAT_HR_RE.match(line.strip()):
            current = trim_blank_edges(current)
            if current:
                blocks.append(current)
            current = []
            continue
        current.append(line)
    current = trim_blank_edges(current)
    if current:
        blocks.append(current)
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


def parse_wechat_reading_export(text: str, source_type: str, source_path: str | None) -> dict | None:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    lines = trim_blank_edges(lines)
    separator_index = next((index for index, line in enumerate(lines) if line.strip() == "---"), None)
    if separator_index is None:
        return None

    header_lines = [line.strip() for line in lines[:separator_index] if line.strip()]
    body_lines = lines[separator_index + 1 :]
    if len(header_lines) < 2:
        return None

    book_title = header_lines[0]
    author = header_lines[1]
    declared_note_count: int | None = None
    reading_started_at: datetime | None = None
    reading_ended_at: datetime | None = None

    for line in header_lines[2:]:
        count_match = WECHAT_NOTE_COUNT_RE.match(line)
        if count_match:
            declared_note_count = int(count_match.group(1))
            continue
        time_match = WECHAT_META_TIME_RE.match(line)
        if time_match:
            label, value = time_match.groups()
            parsed = parse_local_datetime(value)
            if parsed is None:
                continue
            if label == "开始时间":
                reading_started_at = parsed
            elif label == "结束时间":
                reading_ended_at = parsed

    if reading_ended_at is None:
        return None
    if not any(WECHAT_CHAPTER_RE.match(line.strip()) for line in body_lines):
        return None

    blocks = split_wechat_blocks(body_lines)
    notes: list[dict] = []
    current_chapter: str | None = None

    for block in blocks:
        block = trim_blank_edges(block)
        if not block:
            continue

        first_line = next((line.strip() for line in block if line.strip()), "")
        chapter_match = WECHAT_CHAPTER_RE.match(first_line)
        if chapter_match:
            current_chapter = chapter_match.group(1).strip()
            block = trim_blank_edges(block[1:])
            if not block:
                continue
        elif current_chapter is None:
            continue

        content_lines: list[str] = []
        for line in block:
            stripped = line.rstrip()
            if not stripped.strip():
                content_lines.append("")
                continue
            stripped = stripped.lstrip()
            if stripped.startswith(">"):
                stripped = stripped[1:]
                if stripped.startswith(" "):
                    stripped = stripped[1:]
            content_lines.append(stripped.rstrip())

        content = "\n".join(content_lines).strip()
        if not content:
            continue

        created_at = format_local_datetime(reading_ended_at + timedelta(seconds=len(notes)))
        note_body = f"章节：**{current_chapter}**\n\n{content}" if current_chapter else content
        notes.append(
            {
                "content": note_body,
                "created_at": created_at,
                "tag": None,
                "chapter": current_chapter,
                "book_title": book_title,
                "author": author,
                "reading_started_at": format_local_datetime(reading_started_at) if reading_started_at else None,
                "reading_ended_at": format_local_datetime(reading_ended_at),
                "source_path": source_path,
                "source_type": "wechat_md" if source_type == "md" else source_type,
                "source_format": "wechat_reading_markdown",
            }
        )

    return {
        "source_path": source_path,
        "source_type": "wechat_md" if source_type == "md" else source_type,
        "source_format": "wechat_reading_markdown",
        "book_title": book_title,
        "author": author,
        "reading_started_at": format_local_datetime(reading_started_at) if reading_started_at else None,
        "reading_ended_at": format_local_datetime(reading_ended_at),
        "declared_note_count": declared_note_count,
        "note_count": len(notes),
        "notes": notes,
    }


def parse_input(text: str, source_type: str, source_path: str | None) -> dict:
    if source_type in {"md", "markdown"} or source_type == "pasted":
        if any(token in text for token in ("阅读周期:", "## ", "<hr/>", "<hr />")):
            parsed = parse_wechat_reading_export(text, source_type, source_path)
            if parsed is not None:
                return parsed
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
