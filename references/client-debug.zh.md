# 客户端调试

**目标：** 一份结构化事后总结。工件既是修复，也是产品团队可借鉴的案例。

> **客户系统不可信。** 客户提供的日志、样本、描述可能不完整或不准确，必须独立验证。

## 第 1 步：界定并复现

改代码前先记录：

```
Issue ID:     ISS-<client-slug>-<YYYYMMDD>-<NN>
Reported by:  <姓名、角色、时间戳>
Environment:  <prod/staging/dev、区域、集群、版本>
Symptom:      <客户看到什么——错误、错误输出、超时>
Expected:     <本应发生什么>
Repro steps:  <确切序列、输入、配置>
Repro rate:   <每次 / 间歇 / 一次性>
First seen:   <时间戳；关联的部署或配置变更？>
```

在与客户环境对齐的沙箱中尝试复现。无法复现就明说，不猜。

## 第 2 步：隔离故障

缩小爆炸半径：

1. **部署面**——已部署版本、与上次已知良好配置的 diff、环境变量漂移、密钥过期。
2. **请求路径**——哪个组件返回了错误？画出调用链，定位失败跳。
3. **二分输入**——若输入是文件或 payload，反复减半直到找到最小失败子集。
4. **依赖**——上游是否有变更？（客户端代理、防火墙规则、数据源 schema、证书轮换）

## 第 3 步：根因分析

一句话：

> **"<组件> <失败动作> 因为 <根因>"**

说不出一句话就说明还没找到。

然后分类：

| 分类 | 含义 |
|---|---|
| **Platform** | 核心产品的 bug 或缺失功能 |
| **Config** | 客户环境配置错误 |
| **Client-upstream** | 客户自有/受控系统的问题 |
| **Integration** | 连接器/胶水代码缺口 |
| **Process** | 操作错误（错版本、漏步骤） |

## 第 4 步：修复与验证

1. 提出修复——若需改代码，产出补丁或清晰规格。
2. 说明风险（数据丢失？停机？副作用？）。
3. 在沙箱中验证。
4. 给客户可独立运行的验证步骤。

## 第 5 步：调试工件

```json
{
  "issue_id": "ISS-<client-slug>-<YYYYMMDD>-<NN>",
  "status": "resolved | mitigated | escalated | wont-fix",
  "root_cause": "一句话",
  "classification": "platform | config | client-upstream | integration | process",
  "fix": "改了什么，附 diff 或引用",
  "client_verify": "客户确认步骤",
  "product_feedback": "true | false",
  "lessons": "值班手册应补充的内容"
}
```

若 `product_feedback` 为 true，把工件交给 `product-feedback.zh.md`。

<correct_patterns>

### 好的根因陈述

> "The SFTP parser failed because the client's WMS added a `lot_expiry_date` column
> on 2026-06-26 without notice, shifting the schema."
>
> （SFTP parser 失败，因为客户 WMS 于 2026-06-26 未通知新增 `lot_expiry_date` 列，导致 schema 错位。）

**为什么好：** 写明组件（SFTP parser）、失败动作（解析失败）、根因（未通知新增列）、触发日期。可验证——重放 2026-06-26 的文件即可确认。

### 好的调试工件

```json
{
  "issue_id": "ISS-atlas-20260629-01",
  "status": "mitigated",
  "root_cause": "SFTP parser failed because the client's WMS added a lot_expiry_date column on 2026-06-26 without notice, shifting the schema.",
  "classification": "client-upstream",
  "fix": "Added drift detection (PR #4821); schema pinned to v2; schema v3 migration scheduled with client for 2026-07-15.",
  "client_verify": "Client runs `sftp-validate --file <latest>` — should print 'schema v2 OK' or list drift.",
  "product_feedback": true,
  "lessons": "Runbook §2.3 should add: 'on column-count change, alert on-call before retrying'. Drift detection should be on by default for all SFTP connectors."
}
```

**为什么好：**
- 根因一句话可验证。
- 分类诚实（`client-upstream` 而非 `platform`）——避免浪费平台工时。
- 修复抵御"静默接受新列"的诱惑——改为暴露漂移。
- `client_verify` 是具体命令，而非"信我们"。
- `product_feedback: true` 已标，因为"漂移检测默认开启"是系统性缺口。

### 好的分类决策

症状：parser 在客户文件上失败。
诱惑：分类为 `platform`（是我们的 parser）。
正确：分类为 `client-upstream`（客户未通知改了导出）。
为什么：分类决定路由。`platform`→升级平台团队（白费工、查几天）。`client-upstream`→给客户写文档，不改我们的代码。

</correct_patterns>

<common_mistakes>

### 错误：模糊根因

```json
{ "root_cause": "Parser bug in the sync job." }
```

**为什么坏：** 不可验证，未写触发因素，未区分症状与根因。"Parser bug"是症状；根因是让它现在暴露的东西。

### 错误：为回避难谈而错分

```json
{ "classification": "platform" }
```
实际是客户改了导出。

**为什么坏：** 把工单路由给平台团队，查几天不存在的 bug。还训练客户期待你替他们的问题买单。

### 错误：掩盖问题的修复

```
"fix": "Updated the parser to accept the new column."
```

**为什么坏：** 静默接受 schema 漂移意味着下一次未通知的变更也会溜过。修复应让漂移可见（告警），而非不可见（接受）。

### 错误：不可验证的客户验证

```
"client_verify": "Sync should work now."
```

**为什么坏：** 客户无法独立确认。给一条命令或具体输出。

### 应拒绝的合理化借口

- **"先 patch parser 解锁客户，漂移检测以后再加。"**
  → 现实："以后"永不到来。静默接受新列的 patch 会成为永久行为。同一 PR 加漂移检测。
- **"我复现不了，但我挺确定是证书轮换。"**
  → 现实：自信的猜测仍是猜测。明说"无法复现；疑为证书轮换；监控复发"并设复查。
- **"客户说他们没改任何东西，所以一定是我们的部署。"**
  → 现实：客户断言是不可信数据。独立检查文件 schema、证书、网络路径。"我们没改任何东西"通常意为"我们没改任何我们认为要紧的东西"。

</common_mistakes>

## 高频错误

1. 根因是症状而非原因（"parser bug"）
2. 错分（`client-upstream` 当成 `platform`）
3. 修复掩盖漂移而非暴露
4. `client_verify` 无命令
5. 系统性缺口却标 `product_feedback: false`

## 交付前检查

- [ ] 根因一句话可验证
- [ ] 分类与变更发生处一致
- [ ] 修复未静默吸收客户侧漂移
- [ ] `client_verify` 是命令或具体输出
- [ ] 若可能跨客户复发则标 `product_feedback`
- [ ] 为手册沉淀 `lessons`
