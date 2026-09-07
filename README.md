# Forward Deployed Engineer — Skill Kit v2.0.0

**`forward-deployed-engineer`** — an agent skill for running FDE (Forward Deployed
Engineer) engagements end to end: discover the real problem, freeze a defensible scope,
prove value with a real slice, deploy safely, drive adoption, and turn every
engagement into reusable assets.

行业无关 · Industry-agnostic，双语 · bilingual (EN/CN mirrors)，支持气隙/信创私有化部署 ·
with air-gapped / 信创 on-prem support。

---

## Install / 安装

The skill is a folder with a `SKILL.md` entry + `references/`, `templates/`,
`examples/`, `industry/` and `scripts/`. Mount it as an Agent skill:

- **Claude Code / Claude Agent SDK**: copy or symlink this directory into your
  skills directory (e.g. `~/.claude/skills/` or a project `.claude/skills/`),
  then load it by name `forward-deployed-engineer`. `SKILL.md` is the only entry;
  modules load lazily on demand.
- **Hermes / Cowork**: register the directory as a skill package; point the entry at
  `SKILL.md`.

Self-validation (no install required): run `python scripts/check-align.py --strict`,
which verifies the EN/CN module mirrors, anchors, cross-references, and placeholder
hygiene.

## Capability map / 能力地图

| Module / 模块 | Purpose / 用途 | Gate / 门禁 |
|---|---|---|
| `01-discovery` | find & quantify the real problem / 发现并量化真问题 | — |
| `02-scoping` | freeze result, boundaries & responsibility / 冻结结果、边界与责任 | three-month collar / 范围合同 |
| `03-integration-architecture` | concrete buildable design / 具体可实施的设计 | ADR + risk register + fence slice |
| `04-evaluation` | falsify the value hypothesis / 证伪价值假设 | pre-registered pass conditions + Golden Set |
| `05-pilot-adoption` | controlled real-user pilot / 受控真实用户试点 | fence + UAT + 8 launch gates + adoption |
| `06-deployment-runbook` | day-one-safe operations / 入职第一天可安全执行 | observability + fault injection + rollback |
| `07-client-debug` | structured incident close-out / 结构化排障收尾 | verifiable root cause + regression sample |
| `08-product-feedback` | evaluable, de-identified feedback / 可评估、去标识反馈 | no client names, outcome language |
| `09-retro-assets` | close the 1→N loop / 闭合 1→N 资产闭环 | baseline delta + leverage trend |
| `10-airgap-deploy` | offline / 信创 delivery / 气隙/信创交付 | written isolation level + offline kit |

Eight-stage lifecycle, autonomy levels L0–L3, and gate decisions (continue / revise /
narrow / stop) are defined in [SKILL.md](SKILL.md).

## Design principles / 设计原则

1. **Agent-native:** `SKILL.md` is the single entry point; modules are lazy-loaded; the
   language routes to `.zh.md` or `.md` mirrors automatically. / 给 Agent 用：单入口、按需加载、语言路由。
2. **Union, not pruning (并集不失真):** this kit merges two earlier FDE doc sets —
   *FDE-01* (engineering-complete: hard rules, templates, air-gap, autonomy) and
   *FDE-02* (structure & judgment: unified module skeleton, ontology layer, four-exit
   gates). No unique point from either is dropped; the merged modules may be longer
   than either parent. / 两版并集：FDE-01 工程化最全，FDE-02 结构与判断更新，本文档两方独有要点全部保留。
3. **Teachability:** every module follows one skeleton — 目标 → 输入输出 → 编号步骤 →
   模板/工件 → `<correct_patterns>` → `<common_mistakes>` (incl. rationalizations to
   reject) → 高频错误 TOP → 交付前检查清单 — so `scripts/check-align.py` can verify
   EN/CN alignment mechanically. / 统一骨架，脚本可校验中英对齐。
4. **Single source of truth for templates:** `templates/` holds the forms; module
   bodies reference them instead of embedding, so the two can't drift. / 模板单一事实源，模块只引用不内嵌。
5. **Evidence, not claims:** every gate lists its evidence; every authority promotion
   matches a level of proof; rollback covers image + migration + config + flags; a
   runbook that needs judgment is incomplete. / 只有证据，不靠声明。

## What it is not / 不适用边界

- **Not** core platform feature development, pure model research, or domain
  regulatory/legal interpretation — those belong to other teams/experts. / 非核心产品功能开发、非纯模型研究、非领域监管解释。
- **Not** a substitute for the client's own security/compliance sign-off. / 不替代客户自身的安全/合规签字。
- **Not** a magic automation level: autonomy is always granted against evidence, never
  by default; high-risk / low-confidence / boundary cases route to humans. / 不放权给假设：高风险永远转人工。

## Examples / 样例

- [`examples/wms-sftp-drift/`](examples/wms-sftp-drift/) — logistics anomaly-ticket
  triage (manufacturing/logistics vertical), full 8-stage walkthrough with a real
  schema-drift incident. / 物流异常订单分诊（制造/物流），含 SFTP schema 漂移事故。
- [`examples/gl-recon-drift/`](examples/gl-recon-drift/) — GL reconciliation &
  adjustment pre-review at a city commercial bank `Iris Bank` (finance vertical),
  synthetic/de-identified data, irreversible actions gated by a human auth chain. / 金融总账对账·调账预审（虚构城商行 Iris Bank），不可逆动作全程人工授权门。

## Contributing & license

- See [CONTRIBUTING.md](CONTRIBUTING.md), [CHANGELOG.md](CHANGELOG.md).
- License: [Apache-2.0](LICENSE).