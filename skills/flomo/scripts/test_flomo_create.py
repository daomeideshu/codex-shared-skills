from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

import flomo_common


SCRIPT = Path(__file__).with_name("flomo_create.py")


class BuildPayloadTests(unittest.TestCase):
    def test_payload_matches_current_mcp_schema(self) -> None:
        payload = flomo_common.build_payload("note", "读书笔记/测试", "markdown")

        self.assertEqual(
            payload,
            {"content": "note #读书笔记/测试", "format": "markdown"},
        )

    def test_batch_create_interval_is_at_least_one_second(self) -> None:
        self.assertGreaterEqual(
            getattr(flomo_common, "MIN_CREATE_INTERVAL_SECONDS", 0),
            1.0,
        )


class CreateCliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def test_source_timestamp_requires_manual_confirmation(self) -> None:
        result = self.run_cli(
            "--content",
            "note",
            "--created-at",
            "2026-05-22T10:00:00+08:00",
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("--allow-current-time", result.stderr)

    def test_confirmation_omits_unsupported_created_at(self) -> None:
        result = self.run_cli(
            "--content",
            "note",
            "--format",
            "markdown",
            "--created-at",
            "2026-05-22T10:00:00+08:00",
            "--allow-current-time",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {"content": "note", "format": "markdown"},
        )
        self.assertIn("current server time", result.stderr)


if __name__ == "__main__":
    unittest.main()
