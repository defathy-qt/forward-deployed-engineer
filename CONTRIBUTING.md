# Contributing / 贡献指南

Thanks for helping maintain the forward-deployed-engineer skill kit. This repo is a
bilingual merged document set — the guiding constraint is **union, not pruning**.

## The one rule / 唯一原则

**Merge = union. Do not drop unique content from either source version.** When editing
a module, keep every unique point from FDE-01 and FDE-02, and from this repo's own
prior versions. Merged modules are allowed — even expected — to be longer than either
parent. If you must cut something, record the reason in the union checklist
(`docs/merge-union-checklist.md`).

## Editing modules / 改模块

1. **Keep the unified skeleton** — 目标 → 输入与输出 → 编号步骤 → 模板/工件
   （引用 `templates/`，不内嵌） → `<correct_patterns>` → `<common_mistakes>`
   （含"应拒绝的合理化借口"） → 高频错误 TOP → 交付前检查清单.
2. **Keep the anchors** — `<!--a:stepN-->`, `<!--a:template-->`, `<!--a:top-->`,
   `<!--a:checklist-->` — identical in `.md` and `.zh.md`.
3. **Never break the EN/CN mirror.** Any change to `references/<name>.md` must be
   mirrored in `references/<name>.zh.md` with identical structure.
4. **Templates stay the single source of truth.** Module bodies reference
   `templates/*` instead of embedding forms.
5. **Placeholders carry examples.** Bare `<TBD>` / `<fill-me>` never ships.

## Before submitting / 提交前

- Run the validator: `python scripts/check-align.py --strict`.
- Run the cross-reference check and ensure all linked module names resolve
  (`references/`, `templates/`, `examples/`, `industry/`).
- Commit messages: short, in English; describe *what* and *why* (see CHANGELOG
  conventions). Keep subject under 50 chars for the bilingual repo.

## Style notes / 风格

- Outcome language, not feature language — state the business metric and its delta.
- Every risk pairs with a mitigation; every gate lists its evidence.
- No client-identifiable data anywhere (deduplicating real incidents is mandatory —
  see `08-product-feedback`).
- Keep the tone of the existing modules: concrete, numbered, executable-by-others.

## License

Apache-2.0 — see [LICENSE](LICENSE).