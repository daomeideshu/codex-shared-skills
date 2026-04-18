# flomo 技能

这个技能提供了一套可复用的 flomo 笔记工作流，通过 flomo MCP server 完成查询、写入、导入和去重。

## 作用

- 按关键词、标签、日期或 id 搜索笔记
- 批量获取笔记详情
- 创建和更新笔记
- 从粘贴文本、PDF、TXT、MD 或微信读书导出内容中导入笔记
- 在写入前检测精确重复
- 规范化标签，并在源数据提供时间时保留时间戳

## 适用场景

当你需要下面这些事情时，用这个技能：

- 检索或总结 flomo 笔记
- 从素材中新增笔记
- 安全导入多条内容
- 整理标签或笔记结构
- 避免重复写入

## 关键文件

- `SKILL.md` - 主操作指南
- `references/workflow.md` - 任务流程和决策规则
- `references/wechat-reading.md` - 微信读书导入规则
- `references/flomo-mcp-notes.md` - MCP 连接和传输说明
- `scripts/` - 用于构造 payload、解析、分页和去重的辅助脚本

## 推荐插件

如果你想把微信读书笔记复制到 flomo，这个插件很适合搭配使用：

- [wxread-export](https://github.com/scarqin/wxread-export)

## 说明

- 这个技能设计为保持自包含、便于共享。
- 它不会把本地工作区状态或运行时缓存文件存进共享仓库。
