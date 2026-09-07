# 产品反馈

**目标：** 让反馈**可评估**——产品经理读完就能定优先级，无需追问；可复用模式同时流入资产库（见 `09-retro-assets.md`）。反馈是闭环的上半段，下半段（把它变成可复用资产）在 `09` 里补齐。

> 产品反馈喂给平台团队；可复用资产喂给*下一位 FDE*。两者都必须存在——只有反馈是建议箱，只有资产是信息孤岛。

## 输入与输出

| | |
|---|---|
| 输入 | 调试工件 `ISS-*`、部署笔记、FDE retro、客户请求 |
| 输出 | `FB-<YYYY>-<NNN>` 反馈条目（JSON）、去标识化 evidence、关联资产提案 |
| 下游 | `09-retro-assets.md`（可复用资产化）、产品团队 backlog/Linear/Jira |

## 第 1 步：模式识别 <!--a:step1-->

写任何单个客户的请求前，先查：

1. 是否有其他客户报过？搜历史调试工件、部署笔记、反馈条目。
2. 是否是更深层缺口的症状？（"客户想要自定义报告 X"可能实为"报告模块缺乏可配置性"）
3. 是真正的产品缺口，还是现有功能配更好的文档/配置就能解决？

若第 3 条为"现有功能可解决"，停止——改去归档文档或配置改进。随后评定**通用性**，它决定路由：

| 通用性级别 | 含义 | 路由 |
|---|---|---|
| **单客户** | 某客户的特定定制 | 以配置交付，不进 backlog |
| **可复用模式** | 同一缺口可能出现在 2–3 个以上客户 | 反馈条目；候选资产 |
| **平台能力** | 每次部署都需要 | 反馈条目 + 资产提案，P0/P1 |

## 第 2 步：去标识化并泛化 <!--a:step2-->

去除客户专有标识（名称、行业、合同金额、日期），再泛化：

| 客户特定（不含） | 泛化（含） |
|---|---|
| "Acme Corp 需要连到他们 legacy ERP 的 SOAP 连接器" | "面向暴露 SOAP 的本地遗留系统的连接器框架" |
| "客户 X 的合规团队想要自定义清单" | "合规规则引擎需按辖区配置清单" |
| "客户 Y 的月末结账要 3 天" | "月末结账流程需并行化与增量处理" |

## 第 3 步：影响评估 <!--a:step3-->

| 维度 | 如何评估 |
|---|---|
| **客户数** | 1 / 2-3 / 4+ / "每次新部署" |
| **商务影响** | 阻断续约 / RFP 必备 / 差异化 / 锦上添花 |
| **临时方案成本** | 缺失此功能每次部署消耗的 FDE 工时 |
| **战略契合** | 是 / 部分 / 沾边 |
| **资产杠杆** | 一次修复能否缩短后续 N 次部署（none / parameterizable / productizable） |

## 第 4 步：反馈条目 <!--a:step4-->

```json
{
  "feedback_id": "FB-<YYYY>-<NNN>",
  "title": "一行，面向结果",
  "source": ["ISS-...", "客户 Y 的部署笔记", "FDE retro"],
  "generality": "single-client | reusable-pattern | platform-capability",
  "pattern": "one-off | recurring (N clients) | universal (every deployment)",
  "current_state": "以产品语言描述的缺口",
  "desired_outcome": "结果而非实现",
  "evidence": [
    "Client A: ...（已去标识）",
    "Client B: ...（已去标识）"
  ],
  "proposed_scope": "feature / API / config surface / docs / reusable-asset",
  "impact": {
    "affected_clients": "1 | 2-3 | 4+ | every-deployment",
    "deal_impact": "blocking | required-for-rfp | differentiator | qol",
    "fde_hours_per_deployment": "预估节省工时",
    "asset_leverage": "none | parameterizable | productizable"
  },
  "priority_recommendation": "p0-critical | p1-high | p2-medium | p3-nice-to-have",
  "related_feedback": ["FB-2026-042"],
  "attachments": ["ISS-..."]
}
```

## 第 5 步：关联与归档 <!--a:step5-->

- 来自调试工件？回链 issue ID（模板：`templates/feedback-template.json`）。
- 多条描述同一缺口？合并并记关联 ID。
- 归档到产品团队消费反馈的位置（backlog、Linear、Jira）。
- 若通用性为"可复用模式"或"平台能力"，同一轮在 `09-retro-assets.md` 开对应资产提案。

## 第 6 步：闭环——双向蒸馏把反馈变成资产 <!--a:step6-->

归档的条目还不是资产。若同一缺口反复出现或阻断多个部署，做"双向蒸馏"：产品反馈喂给平台团队，可复用资产喂给*下一位 FDE*：

| 反馈形态 | 产出资产（`09-retro-assets.md`） |
|---|---|
| 反复出现的任务模式 | Skill（可重复步骤） |
| 反复出现的系统连接 | 连接器（产品化集成） |
| 反复出现的评测/方法论缺口 | 模板或测试集（Golden Set 分层） |
| 平台 bug / 缺失能力 | 带证据与 ROI 的产品需求 |

## 模板 / 工件 <!--a:template-->

- `templates/feedback-template.json` —— 反馈条目 JSON（即第 4 步形态）
- 产出 ID：`FB-<YYYY>-<NNN>`

**门禁提示：** evidence 带客户名、写实现而非结果、`pattern` 撒谎、影响未量化 → 条目驳回。归档了却永远不成资产 = 建议箱装满没人看。

<correct_patterns>

### 好的反馈条目（节选）

```json
{
  "feedback_id": "FB-2026-042",
  "title": "Drift detection for SFTP connectors should be on by default",
  "source": ["ISS-atlas-20260629-01", "ISS-beta-20260418-02", "FDE retro 2026-06"],
  "generality": "platform-capability",
  "pattern": "recurring (3 clients in 6 months)",
  "current_state": "SFTP connectors fail silently when client schema changes; drift detection exists but is opt-in.",
  "desired_outcome": "Drift detection on by default for all SFTP connectors, with configurable alert threshold.",
  "evidence": [
    "Client A: unannounced column addition caused 3-day sync failure (de-identified)",
    "Client B: column rename caused silent data loss for 1 batch (de-identified)",
    "Client C: detected drift only because FDE happened to be on-call (de-identified)"
  ],
  "proposed_scope": "config default + alert",
  "impact": {
    "affected_clients": "4+",
    "deal_impact": "differentiator",
    "fde_hours_per_deployment": "3-5h per deployment troubleshooting drift",
    "asset_leverage": "productizable"
  },
  "priority_recommendation": "p1-high",
  "related_feedback": []
}
```

**为什么好：** 标题面向结果；通用性与 pattern 诚实量化并附来源；evidence 跨三个实例去标识；写结果不写 API 形态；影响具体（每次部署 3-5h）加上资产杠杆（PM 可算 ROI）；优先级诚实（P1 而非 P0）。

### 好的去标识化

| 原文（不要归档） | 去标识后（归档） |
|---|---|
| "Acme Corp's WMS added lot_expiry_date on 2026-06-26" | "Client A: unannounced column addition (date withheld)" |
| "Bank ABC's compliance team wants a custom KYC checklist" | "Client B: compliance team needs configurable checklists" |

**为什么好：** 去掉名称、行业、日期，保留技术形态。产品团队无需知道哪个客户即可行动。

</correct_patterns>

<common_mistakes>

### 错误：点名客户

```
"evidence": ["Acme Corp's WMS added a column on 2026-06-26..."]
```

**为什么坏：** 违反去标识化。内部工件会被转发给 PM、高管、有时上外部 slide。客户名一旦落字就扩散。

### 错误：写实现

```
"proposed_scope": "Add a `drift_detection_enabled` boolean to the SFTP connector config, default true, with a `drift_alert_threshold` int field..."
```

**为什么坏：** 规定了 API 形态。产品团队可能有更好的设计（事件驱动，而非 boolean）。描述结果（"drift detection on by default"），而非实现。

### 错误：抬高级别

```
"priority_recommendation": "p0-critical"
```
用在锦上添花项上。

**为什么坏：** 训练产品团队忽视你的优先级。真 P0（数据丢失、安全）来时被虚假 P0 淹没。

### 错误：在 `pattern` 上撒谎

```
"pattern": "recurring (N clients)"
```
实际只一个客户报，但是大客户。

**为什么坏：** `pattern` 量化广度。在此撒谎误导优先级且侵蚀字段可信度。真相是"one-off (large client, high ARR)"就写——那仍是有用信号。

### 应拒绝的合理化借口

- **"我标 P0 他们才会真看。"**
  → 现实：喊狼来了的 P0 训练团队忽视你。真 P0 来时被淹没。"重要但不阻断"用 P1-high——仍会被看到。
- **"只一个客户，但是大客户，所以我写'recurring'。"**
  → 现实：pattern 字段量化客户数。撒谎误导优先级且侵蚀字段可信度。真相是"one-off (large client)"就写。
- **"我把实现写出来他们直接建——省一轮来回。"**
  → 现实：你是 FDE 不是产品负责人。你的 evidence 塑造规格；产品团队拥有设计。错的实现比对的 outcome 更费时。
- **"客户请求太多，先归档再说，资产化以后再补。"**
  → 现实："以后"永不到来。归档即完成的心态会把反馈变成没人读的建议箱——归档的同时蒸馏。

</common_mistakes>

## 高频错误 <!--a:top-->

1. evidence 中出现客户名
2. 写实现而非结果
3. 优先级抬高（非阻断项标 P0）
4. `pattern` 字段撒谎（单次写成 recurring）
5. 无 `fde_hours_per_deployment`——影响未量化
6. 可复用模式没有关联资产提案（归档了却从未变成资产）

## 交付前检查 <!--a:checklist-->

- [ ] 无客户名、行业、合同金额
- [ ] 标题面向结果非实现
- [ ] 通用性级别与 `pattern` 诚实量化
- [ ] `impact` 四字段齐全，含资产杠杆
- [ ] 优先级与 evidence 相称
- [ ] 回链源调试工件（`ISS-*` 源）
- [ ] 可复用/平台级缺口已附带对应资产提案并蒸馏进 09