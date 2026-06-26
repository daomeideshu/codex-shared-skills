#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys

from flomo_common import build_payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a flomo create payload")
    parser.add_argument("--content", required=True, help="Note body")
    parser.add_argument("--tag", help="Destination tag path, with or without leading #")
    parser.add_argument("--format", help="flomo format value, such as markdown")
    parser.add_argument(
        "--created-at",
        help="Source timestamp metadata; unsupported by the current MCP create schema",
    )
    parser.add_argument(
        "--allow-current-time",
        action="store_true",
        help="Confirm creation with the server current time when --created-at is supplied",
    )
    args = parser.parse_args()

    if args.created_at and not args.allow_current_time:
        parser.error(
            "the current flomo MCP cannot set created_at; rerun with "
            "--allow-current-time only after manual confirmation"
        )
    if args.created_at:
        sys.stderr.write(
            "Warning: created_at is unsupported and was omitted; "
            "flomo will use the current server time.\n"
        )

    payload = build_payload(args.content, args.tag, args.format)
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
