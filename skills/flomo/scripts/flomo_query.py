#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys


def split_ids(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def build_search_payload(args: argparse.Namespace) -> dict[str, object]:
    payload: dict[str, object] = {}
    if args.keywords:
        payload["keywords"] = args.keywords.strip()
    if args.tag:
        payload["tag"] = args.tag.strip()
    if args.start_date:
        payload["start_date"] = args.start_date.strip()
    if args.end_date:
        payload["end_date"] = args.end_date.strip()
    if args.limit is not None:
        payload["limit"] = args.limit
    if args.has_tag:
        payload["has_tag"] = True
    return payload


def build_get_payload(args: argparse.Namespace) -> dict[str, object]:
    payload: dict[str, object] = {}
    if args.id:
        payload["id"] = args.id.strip()
    elif args.ids:
        payload["ids"] = split_ids(args.ids)
    else:
        raise SystemExit("either --id or --ids is required")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Build flomo query arguments")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Build memo_search arguments")
    search_parser.add_argument("--keywords", help="Free-text search keywords")
    search_parser.add_argument("--tag", help="Exact tag path")
    search_parser.add_argument("--start-date", help="Inclusive start date")
    search_parser.add_argument("--end-date", help="Inclusive end date")
    search_parser.add_argument("--limit", type=int, help="Maximum number of results")
    search_parser.add_argument("--has-tag", action="store_true", help="Only return notes with tags")

    get_parser = subparsers.add_parser("get", help="Build memo_batch_get arguments")
    get_parser.add_argument("--id", help="Single note id")
    get_parser.add_argument("--ids", help="Comma-separated note ids")

    args = parser.parse_args()

    if args.command == "search":
        payload = build_search_payload(args)
    elif args.command == "get":
        payload = build_get_payload(args)
    else:
        raise SystemExit(f"unsupported command: {args.command}")

    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
