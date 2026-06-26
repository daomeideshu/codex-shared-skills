# WeChat Reading API Sync

Use this workflow only when syncing notes directly from 微信读书 through the official `weread-skills` API skill.

Do not use this workflow for local WeChat Reading markdown exports. Those exports are no longer the preferred WeChat Reading path.

## Prerequisites
- The official `weread-skills` skill is installed.
- `WEREAD_API_KEY` is available from the environment or the active WeRead skill runtime.
- Do not write the API key into flomo notes, skill files, logs, or user-facing output.

## Source
- Use `/user/notebooks` to find books with notes.
- Use `/book/bookmarklist` for a selected `bookId` to fetch highlights and chapter metadata.
- Use the API-provided book title, chapter title, highlight text, note/comment text, and item timestamp.

## flomo Format
Each synced item must use only this body shape:

```text
章节：章节名

摘录或笔记内容

#目标标签
```

Do not add:
- Book title line
- Author line
- Source URL or `weread://` link
- API metadata such as `bookId`, `chapterUid`, or range
- Extra tags such as `#微信读书/高亮`
- Markdown bold around the chapter name

## Tags
- Build target tag from your own reading-note tag tree.
- Use a placeholder pattern such as `<根标签>/<分类>/<书名>` if you need a template.
- Resolve the category from the existing tag tree first.
- If no clear category exists, stop and ask for confirmation.
- Do not create a new top-level category automatically.

## Timestamps
- Convert source Unix seconds to local `+08:00` time and keep them in preview/checkpoint metadata.
- Use source time as `created_at` only when the exposed `memo_create` schema supports it.
- Otherwise ask for explicit confirmation to write the identified batch with current server time.
- After confirmation, create serially and wait at least 1 second after each successful response before sending the next item.

## Dedup and Batch Safety
- Before creating a note, search flomo for a distinctive excerpt from the final content.
- Treat only exact normalized final-body matches as duplicates.
- For batch sync, create one representative sample first and wait for user confirmation before continuing.
- After confirmation, continue from the next unsynced item, not from the beginning.
