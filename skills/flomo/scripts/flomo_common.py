#!/usr/bin/env python3
from __future__ import annotations

import re

WHITESPACE_RE = re.compile(r"[ \t]+")
TAG_SEGMENT_RE = re.compile(r"[^\w\u4e00-\u9fff]+", re.UNICODE)
MIN_CREATE_INTERVAL_SECONDS = 1.0


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u3000", " ")
    lines = [WHITESPACE_RE.sub(" ", line).strip() for line in text.split("\n")]
    out: list[str] = []
    previous_blank = False
    for line in lines:
        if not line:
            if out and not previous_blank:
                out.append("")
            previous_blank = True
            continue
        out.append(line)
        previous_blank = False
    return "\n".join(out).strip()


def normalize_tag_segment(segment: str) -> str:
    cleaned = TAG_SEGMENT_RE.sub("_", segment.strip())
    cleaned = re.sub(r"_+", "_", cleaned)
    return cleaned.strip("_")


def normalize_tag_path(tag: str) -> str:
    value = tag.strip()
    if value.startswith("#"):
        value = value[1:]
    parts = [normalize_tag_segment(part) for part in value.split("/")]
    parts = [part for part in parts if part]
    return "/".join(parts)


def build_note_body(content: str, chapter: str | None = None) -> str:
    body = content.strip()
    if chapter:
        return f"章节：**{chapter}**\n\n{body}"
    return body


def build_payload(content: str, tag: str | None, format_name: str | None) -> dict:
    body = content.strip()
    if tag:
        normalized_tag = normalize_tag_path(tag)
        tag_text = f"#{normalized_tag}" if normalized_tag else ""
        if tag_text and tag_text not in body:
            body = f"{body} {tag_text}".strip()
    payload = {
        "content": body,
    }
    if format_name:
        payload["format"] = format_name
    return payload
