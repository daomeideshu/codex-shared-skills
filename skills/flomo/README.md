# flomo Skill

This skill provides a reusable workflow for working with flomo notes through the flomo MCP server.

这个 skill 提供了一套可复用的 flomo 笔记工作流，通过 flomo MCP server 来完成查询、写入、导入和去重。

## What It Does / 作用

- Search notes by keyword, tag, date, or id
- Fetch note details in batches
- Create and update notes
- Import notes from pasted text, PDF, TXT, MD, or WeChat Reading exports
- Detect exact duplicates before writing
- Normalize tags and preserve timestamps when source data provides them

- 按关键词、标签、日期或 id 搜索笔记
- 批量获取笔记详情
- 创建和更新笔记
- 从粘贴文本、PDF、TXT、MD 或微信读书导出内容中导入笔记
- 在写入前检测精确重复
- 规范化标签，并在源数据提供时间时保留时间戳

## When To Use It / 适用场景

Use this skill when you want to:

- retrieve or summarize flomo notes
- add new notes from source material
- import multi-note content safely
- clean up tags or note organization
- avoid duplicate writes

当你需要下面这些事情时，用这个 skill：

- 检索或总结 flomo 笔记
- 从素材中新增笔记
- 安全导入多条内容
- 整理标签或笔记结构
- 避免重复写入

## Key Files / 关键文件

- `SKILL.md` - main operating guide
- `references/workflow.md` - task flow and decision rules
- `references/wechat-reading.md` - import rules for WeChat Reading exports
- `references/flomo-mcp-notes.md` - MCP connection and transport notes
- `scripts/` - helper scripts for payload building, parsing, pagination, and deduplication

- `SKILL.md` - 主操作指南
- `references/workflow.md` - 任务流程和决策规则
- `references/wechat-reading.md` - 微信读书导入规则
- `references/flomo-mcp-notes.md` - MCP 连接和传输说明
- `scripts/` - 用于构造 payload、解析、分页和去重的辅助脚本

## Recommended Plugin / 推荐插件

For copying WeChat Reading notes into flomo, a useful companion plugin is:

如果你想把微信读书笔记复制到 flomo，这个插件很适合搭配使用：

- [wxread-export](https://github.com/scarqin/wxread-export)

## Notes / 说明

- This skill is designed to stay self-contained and shareable.
- It avoids storing local workspace state or runtime cache files in the shared repo.

- 这个 skill 设计为保持自包含、便于共享。
- 它不会把本地工作区状态或运行时缓存文件存进共享仓库。
