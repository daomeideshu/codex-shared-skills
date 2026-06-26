# flomo MCP Notes

## Connection and auth
- Use the active flomo MCP server at `https://flomoapp.com/mcp`.
- Treat OAuth and connection state as transport-layer concerns, not note-format concerns.
- If the client shows `Auth required`, refresh or re-establish the MCP connection before retrying note writes.
- Keep all connection, login, and retry notes in this file only.

## Common operations
- `memo_search`: query notes by keyword, tag, or filters
- `memo_batch_get`: fetch full note content by id
- `memo_create`: create a note with inline tags; the current schema accepts `content` and optional `format`
- `memo_update`: update an existing note body
- `tag_search`, `tag_tree`, `tag_rename`: inspect and manage tags

## Writing notes
- Do not probe `tools/list` on every normal request. Trust the current thread schema until a parameter fails or the result contradicts it.
- The current service schema does not expose `created_at` for `memo_create`.
- If source timestamps matter, keep them in preview metadata and obtain manual confirmation before using current server time.
- For confirmed batches, create serially and wait at least 1 second after each successful response.
- If a future schema exposes `created_at`, test one sample and verify the returned time before continuing the batch.
- Keep note body plain; flomo supports a small subset of formatting.

## Reading notes
- Prefer compact summaries in query responses.
- Show `id`, `created_at`, `tags`, and a short excerpt for each hit.
- Follow `references/workflow.md` for time-based pagination policy.

## Transient failures
- Retry transport errors, timeouts, and 5xx responses.
- Do not retry auth errors, validation errors, or user rejections.
- Prefer short backoff intervals between attempts.
