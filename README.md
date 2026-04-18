# codex-shared-skills

这是一个用于共享 Codex skills 的仓库，适合把可复用的工作流、脚本和说明集中管理，再分发到不同项目里使用。

## 已包含的 Skill

- `skills/flomo` - 用于查询、新建、导入、去重和整理 flomo 笔记

## 仓库结构

- `skills/` - 每个 skill 独立一个目录
- `prompts/` - 可选的提示词资产或角色辅助文件
- `docs/` - 约定、使用说明和维护文档

## Skill 推荐结构

```text
skills/<skill-name>/
  README.md
  SKILL.md
  scripts/
  references/
  assets/
  examples/
```

## 如何在 Codex 中安装

如果你想在本机 Codex 里使用这个仓库中的 skill，最直接的做法是把目标 skill 目录复制到 Codex 的本地 skills 目录。

### 在 Codex App 里用 GitHub 地址安装

如果你的 Codex App 支持 `skill install`，可以直接使用这个仓库的 GitHub 地址安装单个 skill：

```text
skill install https://github.com/daomeideshu/codex-shared-skills/tree/main/skills/flomo
```

如果你要安装仓库里的其他 skill，把路径里的 `flomo` 换成对应目录名即可。

### 安装脚本方式

如果你更习惯用脚本，也可以使用官方 skill installer 的 GitHub 安装脚本：

```powershell
python C:\Users\admin\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py --url https://github.com/daomeideshu/codex-shared-skills/tree/main/skills/flomo
```

### 安装单个 Skill

以 `flomo` 为例：

```powershell
$codexSkills = Join-Path $env:USERPROFILE ".codex\skills"
New-Item -ItemType Directory -Force -Path $codexSkills | Out-Null
Copy-Item -Recurse -Force ".\skills\flomo" "$codexSkills\flomo"
```

复制完成后，重启 Codex，或重新加载 skills 列表，即可使用 `$flomo`。

### 安装整个仓库

如果以后仓库里还会继续增加别的 skills，可以一次性复制整个 `skills/` 目录：

```powershell
$codexSkills = Join-Path $env:USERPROFILE ".codex\skills"
New-Item -ItemType Directory -Force -Path $codexSkills | Out-Null
Copy-Item -Recurse -Force ".\skills\*" $codexSkills
```

### 验证安装

- 检查目标目录下是否出现 `flomo\SKILL.md`
- 在 Codex 里直接输入 `$flomo` 测试是否能唤起该 skill

## 说明

- 这个仓库会尽量保持 skill 自包含，方便复制和复用。
- 不建议把本地运行缓存、私有密钥或个人工作区状态提交进来。
