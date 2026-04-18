# flomo MCP Notes

## Connection and auth
- Use the active flomo MCP server at `https://flomoapp.com/mcp`.
- Treat OAuth and connection state as transport-layer concerns, not note-format concerns.
- If the client shows `Auth required`, refresh or re-establish the MCP connection before retrying note writes.
- Keep all connection, login, and retry notes in this file only.

## Common operations
- `memo_search`: query notes by keyword, tag, or filters
- `memo_batch_get`: fetch full note content by id
- `memo_create`: create a note with inline tags and optional `created_at`
- `memo_update`: update an existing note body
- `tag_search`, `tag_tree`, `tag_rename`: inspect and manage tags

## Writing notes
- Use RFC3339 timestamps when backfilling `created_at`.
- If server refuses backfilled timestamps, report that before writing more notes.
- Keep note body plain; flomo supports a small subset of formatting.

## Reading notes
- Prefer compact summaries in query responses.
- Show `id`, `created_at`, `tags`, and a short excerpt for each hit.
- Follow `references/workflow.md` for time-based pagination policy.

## Transient failures
- Retry transport errors, timeouts, and 5xx responses.
- Do not retry auth errors, validation errors, or user rejections.
- Prefer short backoff intervals between attempts.
