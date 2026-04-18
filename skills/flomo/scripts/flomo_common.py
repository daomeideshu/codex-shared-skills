#!/usr/bin/env python3
from __future__ import annotations

import re

WHITESPACE_RE = re.compile(r"[ \t]+")
TAG_SEGMENT_RE = re.compile(r"[^\w\u4e00-\u9fff]+", re.UNICODE)


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


def coerce_created_at(value: str | None) -> str | None:
    if not value:
        return None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return f"{value}T00:00:00+08:00"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", value):
        return f"{value}+08:00"
    return value


def build_note_body(content: str, chapter: str | None = None) -> str:
    body = content.strip()
    if chapter:
        return f"章节：**{chapter}**\n\n{body}"
    return body


def build_payload(content: str, tag: str | None, created_at: str | None) -> dict:
    body = content.strip()
    if tag:
        normalized_tag = normalize_tag_path(tag)
        tag_text = f"#{normalized_tag}" if normalized_tag else ""
        if tag_text and tag_text not in body:
            body = f"{body} {tag_text}".strip()
    payload = {
        "content": body,
    }
    normalized_created_at = coerce_created_at(created_at)
    if normalized_created_at:
        payload["created_at"] = normalized_created_at
    return payload
