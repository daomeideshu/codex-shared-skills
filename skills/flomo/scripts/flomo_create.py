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
    parser.add_argument("--created-at", help="RFC3339 or date-only value")
    args = parser.parse_args()

    payload = build_payload(args.content, args.tag, args.created_at)
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
