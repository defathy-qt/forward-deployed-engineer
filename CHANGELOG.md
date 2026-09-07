# Changelog

## [2.0.0] — 2026-09-07

### Merged / 合并

Unified two earlier FDE delivery sets into one bilingual agent skill.
将早期两版 FDE 交付文档合并为一套双语 Agent 技能。

- **Source FDE-01** — engineering-complete package (hard rules, 16 templates, air-gap,
  autonomy L0–L3, on-site debugging).
- **Source FDE-02** — reference playbooks (unified module skeleton, discovery/scoping
  split, ontology layer, four-exit gates, adoption metrics).

Both sets remain untouched under `D:\AI\FDE\` as source material.
两原件保留于 `D:\AI\FDE\` 作素材。

### What changed / 变化

- **10-module bilingual structure** (`references/*.md` + `*.zh.md`): FDE-02's combined
  discovery/scoping split into `01` + `02`; `poc-evaluation` renamed `evaluation`;
  `asset-reuse` merged with FDE-02's `retro` into `09-retro-assets`; FDE-01's
  `airgap-deploy` carried as `10`. / 10 模块双语结构，模块命名按合并方案重排。
- **SKILL.md entry** replacing per-tool READMEs: capability model, 8-stage lifecycle,
  18 artifact ID conventions, 7 hard rules, gate decisions, autonomy levels, module
  routing, language routing. / 新增 SKILL.md 唯一入口。
- **Unified module skeleton** + anchors (`<!--a:stepN-->` etc.) so `check-align.py`
  verifies EN/CN mirrors mechanically. / 统一骨架与 anchor，脚本可校验。
- **Templates** : all 16 FDE-01 templates retained (IDs re-checked); `deployment-runbook.md`
  added as the runbook skeleton that module 06 references (module body is the live example).
  / 16 模板全保留；新增部署手册骨架模板，供模块 06 引用。
- **Examples** : `wms-sftp-drift` retained (module references updated); **new**
  `gl-recon-drift` — Iris Bank GL reconciliation & adjustment pre-review, full 8-stage,
  synthetic data, human auth gate, reuses `connector-sftp-watcher` to teach 1→N. /
  保留物流样例，新增金融样例。
- **Industry profiles** : manufacturing / finance / government retained with updated
  module references. / 三份行业画像保留并更新引用。
- **Tooling** : merged `check-align.py` (fence stripping, cross-reference resolution,
  placeholder hygiene, anchor-seq parity, length ratio, `--json` / `--strict`) + CI
  workflow + PR/Issue templates. / 合并版校验脚本与 CI。

### Removed / 移除

None — merge = union (并集不失真). The per-module union trace and validation evidence
are recorded in `docs/merge-union-checklist.md`. / 无删除；逐模块并集对照与校验证据见
并集对照清单。

---

## [Unreleased]

- Planned: install packaging for Hermes / Cowork (currently package + self-check only).