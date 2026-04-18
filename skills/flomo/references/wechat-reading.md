# WeChat Reading Export

Use this only for markdown exports from 微信读书.

## Structure
- First line: book title.
- Second line: author.
- Reading metadata includes `开始时间` and `结束时间`.
- `---` separates metadata from notes.
- `##` lines are chapter headings.
- Each `<hr/>` separated quote block is one note.

## Normalization
- Put `章节：**章节名**` on the first line of every note body.
- Use `结束时间` as base `created_at`.
- Add one second per note in source order.

## Tags
- Build target tag as `读书笔记/分类/书名`.
- Resolve `分类` from existing `读书笔记` tree first.
- If no clear match exists, stop and ask for confirmation.
- Do not create a new category or leaf tag automatically.
