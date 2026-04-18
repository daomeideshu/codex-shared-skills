# flomo Skill

This skill provides a reusable workflow for working with flomo notes through the flomo MCP server.

## What It Does

- Search notes by keyword, tag, date, or id
- Fetch note details in batches
- Create and update notes
- Import notes from pasted text, PDF, TXT, MD, or WeChat Reading exports
- Detect exact duplicates before writing
- Normalize tags and preserve timestamps when source data provides them

## When To Use It

Use this skill when you want to:

- retrieve or summarize flomo notes
- add new notes from source material
- import multi-note content safely
- clean up tags or note organization
- avoid duplicate writes

## Key Files

- `SKILL.md` - main operating guide
- `references/workflow.md` - task flow and decision rules
- `references/wechat-reading.md` - import rules for WeChat Reading exports
- `references/flomo-mcp-notes.md` - MCP connection and transport notes
- `scripts/` - helper scripts for payload building, parsing, pagination, and deduplication

## Notes

- This skill is designed to stay self-contained and shareable.
- It avoids storing local workspace state or runtime cache files in the shared repo.
