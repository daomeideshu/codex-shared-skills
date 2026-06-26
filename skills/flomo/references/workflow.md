# Workflow

## 1. Classify the request
- Query: search existing notes and return compact results first.
- Create: build one note body and write it to flomo.
- Import: extract notes from pasted text or files, then create notes one by one.
- Dedup: compare the final body that will be written before creating notes.

## 2. Normalize input
- Read from file when a file path is provided.
- Read from pasted text when the user pastes content directly.
- Use one memo block per note.
- Preserve source dates when they exist.
- For 微信读书, sync directly through the official WeRead API skill and read `references/wechat-reading.md`; do not use local markdown export parsing.

## 3. Resolve tags before writing
- Keep the requested tag path as destination unless source format defines one.
- Suggest at most two existing tags when tag help is needed.
- Stop and ask for confirmation before creating a new tag or category.
- Replace spaces and forbidden punctuation with `_` in all tag segments.
- Do not use emoji in tags.

## 4. Query before writing
- Search by tag or keywords when the user asks to avoid duplicates.
- Use batch get when you already have ids and need full content.
- When retrieving many notes, page by time in chunks of at most 50 items.
- Compute a time step from current time span and remaining note count so each page stays under 50.
- If a page still reaches 50 items, shrink the window and retry before advancing.
- Keep pagination as a query-only helper.

## 5. Write notes
- Use `created_at` only when it is present in the exposed `memo_create` schema.
- When source time exists but `created_at` is unsupported, show the source time in the preview and ask for explicit confirmation to write with the current server time.
- After confirmation, send create calls serially and wait at least 1 second after each successful response before the next call.
- If a timestamp parameter is rejected or ignored, stop and inspect the detailed MCP schema before continuing.
- For transient MCP failures, follow `references/flomo-mcp-notes.md`.

## 6. Batch import
- Verify one sample note first when source contains multiple entries.
- After sample is accepted, continue with the rest.
- Report skipped duplicates with their matching source text.
