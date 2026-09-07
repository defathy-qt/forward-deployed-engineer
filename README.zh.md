# 前沿部署工程师（FDE）技能包 v2.0.0

**`forward-deployed-engineer`** —— 一套给 Agent 用的 FDE（前沿部署工程师）全生命周期技能：发现真问题、冻结可辩护范围、用真实链路证明价值、安全上线、推动采用、把每次交付沉淀为可复用资产。

行业无关 · Industry-agnostic，双语 · bilingual（中英镜像），支持气隙/信创私有化部署 · with air-gapped / 信创 on-prem support。

---

## 安装

技能包由 `SKILL.md` 入口 + `references/`、`templates/`、`examples/`、`industry/`、`scripts/` 组成。以 Agent 技能方式挂载：

- **Claude Code / Claude Agent SDK**：把本目录复制或软链到技能目录（如 `~/.claude/skills/` 或项目的 `.claude/skills/`），按名字 `forward-deployed-engineer` 加载。`SKILL.md` 是唯一入口，模块按需懒加载。
- **Hermes / Cowork**：将目录注册为技能包，入口指向 `SKILL.md`。

自检（无需安装）：运行 `python scripts/check-align.py --strict`，校验中英模块镜像、anchor、交叉引用与占位符卫生。

## 能力地图

| 模块 | 用途 | 门禁 |
|---|---|---|
| `01-discovery` | 发现并量化真问题 | — |
| `02-scoping` | 冻结结果、边界与责任 | 范围合同 |
| `03-integration-architecture` | 具体可实施的设计 | ADR + 风险登记 + PoC 切片 |
| `04-evaluation` | 证伪价值假设 | 先验通过条件 + Golden Set |
| `05-pilot-adoption` | 受控真实用户试点 | 围栏 + UAT + 八项上线门禁 + 采用 |
| `06-deployment-runbook` | 入职第一天可安全执行 | 可观测 + 故障注入 + 回滚 |
| `07-client-debug` | 结构化排障收尾 | 可验证根因 + 回归样本 |
| `08-product-feedback` | 可评估、去标识反馈 | 无客户名、结果语言 |
| `09-retro-assets` | 闭合 1→N 资产闭环 | 基线差值 + 杠杆趋势 |
| `10-airgap-deploy` | 气隙/信创交付 | 书面隔离等级 + 离线包 |

八阶段生命周期、放权等级 L0–L3、门禁四出口（继续/修订/收窄/停止）见 [SKILL.md](SKILL.md)。

## 设计原则

1. **给 Agent 用：** `SKILL.md` 唯一入口，模块懒加载，语言自动路由到中/英镜像。 / Agent-native: single entry, lazy loading, language routing.
2. **并集不失真：** 本包合并早期两版 FDE 文档——*FDE-01*（工程化最全：硬规则、模板、气隙、放权）与 *FDE-02*（结构与判断更新：统一骨架、本体层、四出口门禁）。两方独有要点全部保留，合并后的模块允许比两原版都长。 / Union of two earlier sets.
3. **可教学：** 每个模块统一骨架——目标→输入输出→编号步骤→模板/工件→正例→反例（含"应拒绝的合理化借口"）→高频错误 TOP→交付前检查——`scripts/check-align.py` 可机械校验中英对齐。 / Teachable, script-checkable.
4. **模板单一事实源：** `templates/` 放表单，模块正文只引用不内嵌，两者不可能漂移。 / Templates referenced, never embedded.
5. **只有证据，不靠声明：** 每道门禁列证据；每次放权匹配证据等级；回滚覆盖镜像+迁移+配置+flag；需要判断的手册就是不完整。 / Evidence, not claims.

## 不适用边界

- **非**核心产品功能开发、纯模型研究、领域监管/法律解释——不属于本件（转交相应团队/专家）。
- **不**替代客户自身的安全/合规签字。
- **不**默认放权：放权始终匹配证据；高风险/低置信/边界用例永远转人工。

## 样例

- [`examples/wms-sftp-drift/`](examples/wms-sftp-drift/) — 物流异常订单分诊（制造/物流行业），八阶段完整走读，含真实 SFTP schema 漂移事故。
- [`examples/gl-recon-drift/`](examples/gl-recon-drift/) — 虚构城商行 `Iris Bank` 的总账对账·调账预审（金融行业），数据全部合成/脱敏，不可逆动作全程人工授权门 + 审计链。

## 贡献与许可

- 见 [CONTRIBUTING.md](CONTRIBUTING.md)、[CHANGELOG.md](CHANGELOG.md)。
- 许可：[Apache-2.0](LICENSE)。