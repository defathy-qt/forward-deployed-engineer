# 复盘与资产复用（1→N）

**目标：** 每次交付结束时，都留下*下一个客户*能继承的资产——把一次性现场工作变成递减的边际成本。如果第二个客户的部署成本和第一个一样高，FDE 闭环就没有合上。**只留下一个系统的是外包；留下可复用资产的是 FDE 实践。**

> 带走行业理解，不带客户数据——"会计准则是公开的，账本是私有的"。第 1 个客户造资产，第 N 个客户配资产。

## 输入与输出

| | |
|---|---|
| 输入 | 本轮交付全部工件（范围合同、架构、评测、runbook、调试工件、反馈条目）、部署指标 |
| 输出 | `RETRO-<vertical>-<YYYYMMDD>` 复盘工件、`AM-<domain>-vN.yaml` 资产 manifest、迁移清单、runbook 教训、杠杆趋势 |
| 下游 | 下一客户交付（复用资产）、`08-product-feedback.md`（平台缺口）、`04-evaluation.md`（复用测试集纳入 Golden Set） |

## 第 1 步：对照承诺与交付 <!--a:step1-->

回到 `02-scoping.md` 的基线，记录实际发生了什么。**不要粉饰差距——差距正是教训所在。**

| 一侧 | 内容 |
|---|---|
| 承诺 | scoping 中的基线 → 目标 |
| 已交付 | 生产环境实测结果 |
| 差距 | 变了什么、为什么变 |

## 第 2 步：分离四层——可复用 vs 客户专属 <!--a:step2-->

只有可复用的那一半能带去下一个项目，诚实切分。把每份交付物拆成四层，只有中间两层成为资产：

| 层 | 内容 | 去向 |
|---|---|---|
| 稳定骨架 | 通用流程、接口契约、控制逻辑 | 可复用资产 |
| 行业约束 | 领域规则、术语、合规模式 | 行业画像/资产配置 |
| 客户配置 | 端点、凭证、组织特有取值 | 客户配置，绝不抽离 |
| 不可迁移 | 客户数据、名称、合同、私有文档 | 销毁或留在现场 |

**客户数据不得进入资产：**

- 资产中不得有客户名、人名、标识、合同金额或真实记录。
- 测试数据必须合成或彻底去标识并重新标注。
- 凭证与端点放在客户配置，绝不进资产包。
- 拿不准就不放；缺示例可补，泄露记录不可挽回。

## 第 3 步：资产六要件检验 <!--a:step3-->

候选物六条全部满足才成为资产：

| 要件 | 问题 |
|---|---|
| 输入输出明确 | 输入输出是否有显式契约？ |
| 可配置 | 客户特有取值是否外置到配置？ |
| 版本化 | 是否有语义化版本与变更日志？ |
| 有测试 | 是否带 Golden Set/单元/故障注入测试？ |
| 有边界 | 是否写明适用与不适用场景（`applies_when` / `does_not_apply`）？ |
| 有 Owner | 是否有维护人为变更与问题负责？ |

## 第 4 步：选择资产类型 <!--a:step4-->

| 资产类型 | 示例 | 复用信号 |
|---|---|---|
| 连接器 | SFTP watcher、SOAP 桥、MCP server | 跨客户相同协议/接口 |
| Agent Skill | 分诊 playbook、依据绑定答复流 | 跨客户相同工作流 |
| 模板 | 范围合同、手册、评测报告 | 每次交付相同文档形态 |
| 工程组件 | 漂移检测器、重试/DLQ、审计日志 | 反复需要相同控制逻辑 |
| 规则包 | 合规检查、校验正则 | 同行业相同规则 |
| 参考架构 | 气隙 LLM 拓扑、网络跳点设计 | 相同部署形态 |
| 交付 Playbook | 发现脚本、UAT 脚本、采用计划 | 每次相同的人的流程 |

## 第 5 步：构建版本化资产包 <!--a:step5-->

带 manifest 打包，让下一位 FDE 知道自己在采用什么（模板：`templates/asset-manifest.yaml`，ID：`AM-<domain>-vN.yaml`）：

```yaml
asset_id: connector-sftp-watcher
name: SFTP CSV watcher with schema-pin and drift alert
type: connector
version: 1.2.0
semver_note: "major=破坏性配置；minor=新能力；patch=修复"
inputs: [sftp_endpoint, credentials_ref, schema_contract, schedule]
outputs: [validated_batch, drift_alert]
applies_when: "客户按固定计划经 SFTP 投递 CSV"
does_not_apply: ["流式/Kafka", "二进制格式", "客户主动推送 API"]
config_surface: [host, port, path, key_ref, schema_version, alert_channel]
tests:
  golden_set: assets/connector-sftp-watcher/golden/
  fault_injection: [missing_file, column_drift, malformed_row, duplicate_batch]
provenance:
  born_in_client: "去标识交付 #3"
  reused_by: ["交付 #5", "交付 #7"]
owner: fde-platform-team
changelog: "CHANGELOG.md"
```

## 第 6 步：度量产品杠杆 <!--a:step6-->

复用必须被度量而非声称。核心 KPI 是*单位价值对应的现场投入*随项目递减：

| 指标 | 定义 |
|---|---|
| 复用率 | 新部署中由既有资产组装的比例 |
| 边际 FDE 工时 | 每次交付的现场工时，逐单趋势 |
| 资产覆盖 | 可用资产数 vs 实际需要的资产类型 |
| 缺陷逃逸 | 复用资产被采用后发现的缺陷（应趋降） |
| 产品杠杆 | 交付的业务价值 ÷ 投入现场工时（应趋升） |

```text
Deployment A: <months / hours to value>
Deployment B (same vertical): <months / hours to value>
Direction:  <should be down; if flat, the loop is not working>
```

第 10 个同类项目还和第 1 个一样贵，说明模式没通过试金石。

## 第 7 步：为平台缺口归档产品反馈 <!--a:step7-->

若现场暴露的是*平台*（而非客户）的缺口，按去标识化、面向结果的条目路由到 `08-product-feedback.md`。反方向也一样：反复出现的反馈形态蒸馏成 `09` 的资产，形成双向闭环。

## 第 8 步：写迁移清单 <!--a:step8-->

下一个项目开始时的启动单：

```text
Reuse as-is:  <entry, agent runtime, permission, reply scaffolding>
Rebuild only: <facts, project/source-rights, media, golden set>
Rewrite rules:<what is different for the new vertical>
```

## 第 9 步：更新 runbook 教训 <!--a:step9-->

任何教了你东西的事故 → 写进 runbook 的 lessons，让下一个运维继承。没写下来的现场经验，下个项目就丢了。

## 第 10 步：归档复盘工件 <!--a:step10-->

```json
{
  "retro_id": "RETRO-<vertical>-<YYYYMMDD>",
  "promised_vs_delivered": {"baseline": "...", "target": "...", "actual": "..."},
  "reusable_assets": ["skill:...", "connector:...", "template:...", "testset:..."],
  "client_specific_left_behind": ["...", "..."],
  "product_feedback_filed": ["FB-..."],
  "leverage": {"deployments": 2, "effort_trend": "down | flat | up"},
  "migration_checklist": "...",
  "runbook_lessons_added": ["..."]
}
```

## 模板 / 工件 <!--a:template-->

- `templates/asset-manifest.yaml` —— 资产 manifest（即第 5 步形态）
- `templates/postmortem.md` —— 承接严重事故复盘，教训流入第 9 步
- 产出 ID：`AM-<domain>-vN.yaml`、`RETRO-<vertical>-<YYYYMMDD>`

**门禁提示：** 没对照基线、没诚实切分客户专属、没抽取至少一个资产、没记录杠杆趋势 → 复盘未完成。复盘工件是每轮交付的硬性收尾，不是可选项。

<correct_patterns>

### 好的资产切分

> "复用：飞书入口、Agent 运行时、权限脚手架、回复模式。重建：课程事实、项目/源码权益、黄金题集。留在客户侧：3 条一次性定价规则。"

**为什么好：** 可复用的一半被命名为资产；客户专属的一半留下；不整包复制，下个项目因而不继承某家客户的特例规则。

### 好的杠杆记录

> "项目 A（课程问答）：6 个 FDE 人日到首个价值。项目 B（同模式，营销问答）：2 个 FDE 人日。复用了入口 + 运行时 + 评测脚手架。"

**为什么好：** 单位价值对应的投入下降了；这个数字就是闭环生效的证明。

### 好的资产抽取

> "三个客户都按计划经 SFTP 投递 CSV。抽取参数化的 `connector-sftp-watcher`（schema 契约、计划、告警通道作为配置）；各客户的 host、密钥、列映射留在各自配置；用按 schema 契约合成的文件替换真实样本。"

**为什么好：** 干净分离骨架、行业形态与客户配置；资产由配置驱动；测试数据从构造上就是合成的。

### 好的 Manifest（节选）

```yaml
asset_id: skill-evidence-bound-triage
version: 0.4.0
applies_when: "操作员必须基于受控内部来源带引用作答"
does_not_apply: ["开放网络检索", "无依据的数值预测"]
tests: {golden_set: golden/v3, result_floor: 0.85, unsafe_action_floor: 0}
provenance: {born_in_client: "去标识 #2", reused_by: ["#4", "#6", "#9"]}
owner: fde-platform-team
```

**为什么好：** 边界（`does_not_apply`）与能力同样明确；测试带数值下限；provenance 展示真实复用且不点名；有 Owner。

</correct_patterns>

<common_mistakes>

### 错误：把客户定制复制成资产 / 整包复制

```
"把 Acme 的集成目录复制一份改个名，发给下一个客户。"
```
```
"克隆课程问答，把课程名一换就行。"
```

**为什么坏：** 客户端点、凭证、schema 怪癖、一次性规则和数据都漏进"资产"；下一次部署继承无法解释的行为，还埋着合规事故。抽取骨架，重建场景专属部分，其余全部外置。

### 错误：资产无 Owner 无边界

```
"建个共享文件夹，大家自己去拿好用的脚本。"
```

**为什么坏：** 无版本、无测试、无适用说明、无维护人——这是坟场不是库。没有 Owner 和"不适用边界"，资产会被错用到从未设计过的场景。

### 错误：把复盘当庆功

> "项目做完了，大家辛苦了，下一个。"

**为什么坏：** 只记录胜利的复盘抓不到任何教训。差距（第 1 步）与失败才是最值钱的产出。

### 错误：不测杠杆

> "不知道有没有变便宜——我们就顾着交付。"

**为什么坏：** 没有投入/价值趋势，就分不清 FDE 实践与高端外包。杠杆曲线只有在测量时才看得出来。

### 应拒绝的合理化借口

- **"再多做几个客户就泛化，先复制粘贴。"**
  → 现实：复制粘贴让分歧复利；三份拷贝之后再没有可泛化的共同资产。第二次用到就抽取——那时模式才为真。
- **"只是内部样本文件，真实数据测起来更真实。"**
  → 现实：内部文件夹会被分享、截图、用于演示。无论意图如何，资产里的真实数据就是数据边界违规。用合成数据。
- **"统计复用指标是官僚主义，我们知道自己复用很多。"**
  → 现实：未度量的复用只是感觉。边际工时与复用率是 1→N 闭环真正生效的唯一证据。

</common_mistakes>

## 高频错误 <!--a:top-->

1. 客户配置/数据被复制进"可复用"资产（整包复制含客户规则）
2. 资产缺六要件之一（尤其无 Owner、无 `does_not_apply` 边界）
3. 复盘只记胜利，无差距、无失败
4. 不测杠杆——分不清 FDE 与外包
5. 无语义版本或变更日志
6. 迁移清单未写、runbook 教训未更新 → 下个项目重学同一失败

## 交付前检查 <!--a:checklist-->

- [ ] 承诺 vs 交付已对照基线
- [ ] 交付物已拆为骨架/行业/客户/不可迁移四层；可复用 vs 客户专属已诚实切分
- [ ] 候选物通过资产六要件
- [ ] 已选资产类型；manifest 含 `applies_when` / `does_not_apply`、版本、changelog 与具名 Owner
- [ ] 已附测试（Golden Set/故障注入）与数值下限
- [ ] 零客户数据；样本全部合成或去标识；凭证在客户配置
- [ ] 杠杆（单位价值投入趋势）与复用度量已记录；provenance 去标识更新
- [ ] 平台缺口已按面向结果条目归档到产品反馈
- [ ] 迁移清单已写（复用/重建/改写）
- [ ] runbook 教训已从事故更新
- [ ] 复盘工件已归档并联接