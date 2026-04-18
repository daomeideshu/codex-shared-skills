# codex-shared-skills

Repository for reusable Codex skills that can be shared across projects.

## Included Skills

- `skills/flomo` - query, create, import, deduplicate, and reorganize flomo notes

## Structure

- `skills/` - each skill in its own folder
- `prompts/` - optional prompt assets or role-specific helpers
- `docs/` - conventions, usage notes, and maintenance guidance

## Skill Layout

Recommended layout for a skill:

```text
skills/<skill-name>/
  SKILL.md
  scripts/
  assets/
  examples/
```

Keep shared skills self-contained and documented so they can be copied or reused without additional setup.
