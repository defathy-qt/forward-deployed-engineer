# 产品反馈

**目标：** 让反馈**可评估**——产品经理读完就能定优先级，无需追问。

## 第 1 步：模式识别

写任何单个客户的请求前，先查：

1. 是否有其他客户报过？搜历史调试工件、部署笔记、反馈条目。
2. 是否是更深层缺口的症状？（"客户想要自定义报告 X"可能实为"报告模块缺乏可配置性"）
3. 是真正的产品缺口，还是现有功能配更好的文档/配置就能解决？

若第 3 条为"现有功能可解决"，停止——改去归档文档或配置改进。

## 第 2 步：去标识化并泛化

去除客户专有标识（名称、行业、合同金额、日期），再泛化：

| 客户特定（不含） | 泛化（含） |
|---|---|
| "Acme Corp 需要连到他们 legacy ERP 的 SOAP 连接器" | "面向暴露 SOAP 的本地遗留系统的连接器框架" |
| "客户 X 的合规团队想要自定义清单" | "合规规则引擎需按辖区配置清单" |
| "客户 Y 的月末结账要 3 天" | "月末结账流程需并行化与增量处理" |

## 第 3 步：影响评估

| 维度 | 如何评估 |
|---|---|
| **客户数** | 1 / 2-3 / 4+ / "每次新部署" |
| **商务影响** | 阻断续约 / RFP 必备 / 差异化 / 锦上添花 |
| **临时方案成本** | 缺失此功能每次部署消耗的 FDE 工时 |
| **战略契合** | 是 / 部分 / 沾边 |

## 第 4 步：反馈条目

```json
{
  "feedback_id": "FB-<YYYY>-<NNN>",
  "title": "一行，面向结果",
  "source": ["ISS-...", "客户 Y 的部署笔记", "FDE retro"],
  "pattern": "one-off | recurring (N clients) | universal (every deployment)",
  "current_state": "以产品语言描述的缺口",
  "desired_outcome": "结果而非实现",
  "evidence": [
    "Client A: ...（已去标识）",
    "Client B: ...（已去标识）"
  ],
  "proposed_scope": "feature / API / config surface / docs",
  "impact": {
    "affected_clients": "1 | 2-3 | 4+ | every-deployment",
    "deal_impact": "blocking | required-for-rfp | differentiator | qol",
    "fde_hours_per_deployment": "预估节省工时"
  },
  "priority_recommendation": "p0-critical | p1-high | p2-medium | p3-nice-to-have",
  "related_feedback": ["FB-2026-042"],
  "attachments": ["ISS-..."]
}
```

## 第 5 步：关联与归档

- 来自调试工件？回链 issue ID。
- 多条描述同一缺口？合并并记关联 ID。
- 归档到产品团队消费反馈的位置（backlog、Linear、Jira）。

<correct_patterns>

### 好的反馈条目（节选）

```json
{
  "feedback_id": "FB-2026-042",
  "title": "Drift detection for SFTP connectors should be on by default",
  "source": ["ISS-atlas-20260629-01", "ISS-beta-20260418-02", "FDE retro 2026-06"],
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
    "fde_hours_per_deployment": "3-5h per deployment troubleshooting drift"
  },
  "priority_recommendation": "p1-high",
  "related_feedback": []
}
```

**为什么好：**
- 标题面向结果（"drift detection on by default"），而非"加个 flag"。
- `pattern` 诚实量化（6 个月内 3 个客户，附来源）。
- evidence 去标识——三个具体实例未点名客户。
- `desired_outcome` 描述结果，而非 API 形态。
- 影响具体（每次部署 3-5h）——PM 可算 ROI。
- 优先级诚实（P1 而非 P0——未阻断交易，但确实反复产生成本）。

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

**为什么坏：** `pattern` 量化广度。在此撒谎误导优先级。真相是"one-off (large client, high ARR)"就写——那仍是有用信号。

### 应拒绝的合理化借口

- **"我标 P0 他们才会真看。"**
  → 现实：喊狼来了的 P0 训练团队忽视你。真 P0 来时被淹没。"重要但不阻断"用 P1-high——仍会被看到。
- **"只一个客户，但是大客户，所以我写'recurring'。"**
  → 现实：pattern 字段量化客户数。撒谎误导优先级且侵蚀字段可信度。真相是"one-off (large client)"就写。
- **"我把实现写出来他们直接建——省一轮来回。"**
  → 现实：你是 FDE 不是产品负责人。你的 evidence 塑造规格；产品团队拥有设计。错的实现比对的 outcome 更费时。

</common_mistakes>

## 高频错误

1. evidence 中出现客户名
2. 写实现而非结果
3. 优先级抬高（非阻断项标 P0）
4. `pattern` 字段撒谎（单次写成 recurring）
5. 无 `fde_hours_per_deployment`——影响未量化

## 交付前检查

- [ ] 无客户名、行业、合同金额
- [ ] 标题面向结果非实现
- [ ] `pattern` 诚实量化
- [ ] `impact` 三字段齐全
- [ ] 优先级与 evidence 相称
- [ ] 回链源调试工件
