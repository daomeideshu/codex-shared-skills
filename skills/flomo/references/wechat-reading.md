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
- Build the target tag from your own reading-note tag tree.
- Use a placeholder pattern such as `<根标签>/<分类>/<书名>` if you need a template.
- Resolve the category from your existing tag tree first.
- If no clear match exists, stop and ask for confirmation.
- Do not create a new category or leaf tag automatically.
