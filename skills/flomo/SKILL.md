---
name: flomo
description: Query, create, update, import, deduplicate, and reorganize flomo notes with preserved timestamps and inline tags. Use when the user wants to search flomo, fetch full note details, create or update memos, import notes from pasted text, PDF, TXT, MD, or WeChat Reading markdown exports, reuse or rename tags, avoid duplicates before writing, or clean up flomo note organization.
---

# Flomo

## Overview
Use flomo MCP for note query, note creation, note updates, tag lookup, and file-based imports.

## Quick Route
1. First classify the request as query, create, import, dedup, or tag cleanup.
2. Use the lightest matching tool path:
   - `memo_search` for discovery
   - `memo_batch_get` only when ids are already known
   - `memo_create` for new notes
   - `memo_update` for edits to an existing note
   - `tag_search` or `tag_tree` for tag resolution
   - `tag_rename` only for intentional bulk cleanup
3. Before writing anything, check whether this request needs a confirmation checkpoint.

## Core Capabilities
- Query notes by keyword, tag, date, or id.
- Batch fetch notes in pages of up to 50 items using time-based stepping for query and verification.
- Create one note from pasted text or a normalized memo block.
- Import notes from PDF, TXT, MD, or WeChat Reading markdown exports.
- Check exact duplicates before creating notes.

## Workflow
1. Classify the request as query, create, import, or dedup.
2. Normalize input into memo blocks and preserve source dates when present.
3. Resolve destination tags from existing tag tree before writing.
4. Query existing notes when dedup is needed.
5. Keep batch reads at or below 50 items with time-based pagination.
6. Skip exact duplicates and report skipped items.
7. For missing tags, suggest at most two existing matches.
8. If no existing tag fits, ask for confirmation before creating a new tag.
9. Create notes with RFC3339 `created_at` when source time is available.
10. Verify one sample item before batch importing multi-note input.
11. For poetry or line-break-sensitive notes, always use LF (`\n`) line breaks only; do not use CRLF (`\r\n`) or literal backslash-n text.

## Concrete Rules
- Normalize line endings to LF before dedup or write.
- Compare duplicates against the final body that would be written, not the raw source text.
- Treat only exact normalized matches as auto-skippable duplicates.
- If a note is only similar, report it as a possible duplicate instead of skipping it silently.
- Replace spaces and forbidden punctuation with `_` in tag segments.
- Do not use emoji in tags.
- Keep the requested tag path unless the source format defines a stricter destination rule.
- When formatting matters, read the flomo format guide before composing the final body.

## Confirmation Checkpoints
- Stop and ask before creating a new top-level tag or category.
- Stop and ask when a note is similar but not exactly identical to an existing note.
- Stop and ask when source parsing is messy enough that note boundaries may be wrong.
- Stop and ask before continuing a batch after the server rejects backfilled timestamps.
- For multi-note imports, confirm one sample note before writing the rest.
- The sample note must be written successfully with `memo_create` before any batch import continues.

## Failure Handling
- Retry transport errors, timeouts, and 5xx failures with short backoff.
- Do not retry auth failures, validation failures, or explicit user rejections unchanged.
- If the source file cannot be parsed reliably, switch to preview mode instead of guessing.
- If a page still returns 50 items after time-based stepping, shrink the window and retry before advancing.
- If the client shows `Auth required`, refresh or re-establish the MCP connection before retrying writes.

## Output Contract
- For query requests, return compact results first: `id`, `created_at`, tags, and a short excerpt.
- For create or import requests, report what was created, skipped, or blocked.
- For dedup checks, distinguish exact duplicates from possible near-duplicates.
- When assumptions were made about tags, dates, or note splitting, state them explicitly.

## Source-Specific Rules
- For generic pasted text, TXT, or Markdown, use one memo block per note and preserve source dates when present.
- For WeChat Reading markdown exports, read `references/wechat-reading.md` before import.
- For WeChat Reading imports, put `章节：**章节名**` on the first line of each note body.
- For WeChat Reading imports, use `结束时间` as the base `created_at` and add one second per note in source order.
- For WeChat Reading imports, resolve the target tag from your own reading-note tag tree, and stop if the category or book-level tag has no clear existing match.

## Query Specifics
- Use `memo_search` first for discovery by keyword, tag, or date filters.
- Use `memo_batch_get` only after ids are known and full content is required.
- When reading many notes, keep each page at or below 50 items with time-based stepping.
- If a time window is still too dense, shrink the window and retry before moving on.
- If the first query returns only noisy or weakly related hits, report "no confident match yet" before expanding into broader keyword variants.
- When the user explicitly asks for compact results first, do not spend extra turns on cross-validation unless you already have a strong candidate set to summarize.

## Input Modes
- Pasted text
- PDF, TXT, MD
- WeChat Reading markdown export

## MCP Tools
- `memo_search`, `memo_batch_get`, `memo_create`, `memo_update`
- `tag_search`, `tag_tree`, `tag_rename`
- `get_format_guide`, `get_tag_guide`

## References
- `references/workflow.md`
- `references/wechat-reading.md`
- `references/flomo-mcp-notes.md`

## Scripts
- `scripts/flomo_common.py`
- `scripts/flomo_create.py`
- `scripts/flomo_query.py`
- `scripts/normalize_input.py`
- `scripts/paginate_by_time.py`
- `scripts/dedup_notes.py`
