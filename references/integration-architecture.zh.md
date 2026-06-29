# 集成架构

**目标：** 一份具体可实施的设计，而非演示稿。每个集成点写明协议、认证、数据形态、失败模式。

## 第 1 步：盘点客户系统

对每个相关系统记录：

| 字段 | 示例 |
|---|---|
| 系统名与版本 | "Legacy ERP 2019"、"Internal CRM v4"、"On-prem data warehouse" |
| 部署形态 | 本地 / 私有云 / SaaS / 隔离网络 |
| 持有数据 | 主数据、交易日志、参考数据 |
| 集成接口 | REST、SOAP、SFTP、ODBC、Kafka、纯文件 |
| 认证与网络约束 | 仅 VPN、mTLS、本地 IdP 的 OAuth2、无外网 |
| 数据量与频率 | 每日 50 万行、实时 vs 夜间批 |
| 客户联系人 | 姓名、团队、升级路径 |

## 第 2 步：定义数据流

每条流写明：

```
[源] → [抽取] → [传输] → [转换] → [落地]

Protocol:  REST / SFTP / JDBC / Kafka / file-watch
Auth:      OAuth2 client-credentials / username+key / 等
Schema:    输入列/类型、输出列/类型、校验规则
Cadence:   实时 / 每小时批 / EOD 文件投递
Error:     失败时——重试、DLQ、告警、人工工单
```

## 第 3 步：设计集成层

三件工件：

1. **网络与认证图**——组件、谁跟谁通信、开放端口、逐跳认证。
2. **连接器清单**——每个连接器一行：类型（MCP server / 定制脚本 / 反向 SSH 隧道 / SFTP watcher）、语言、工作量（S/M/L）、可复用性（能否产品化？）。
3. **配置面**——客户管理员部署后需配置的内容（环境变量、密钥、feature flag、白名单）。

## 第 4 步：风险登记

| 风险 | 缓解 |
|---|---|
| 客户 schema 无预告变更 | 锁版本 + 漂移告警 |
| 本地系统计划停机 | 优雅降级；排队重放 |
| 安全审查阻断部署 | 提前备问卷与评审文档 |
| 隔离网络中继延迟 | 尽早压测；书面约定 SLA |

## 第 5 步：产出文档

```markdown
# 集成架构：<客户> — <日期>

## 1. 摘要（3 句话）
## 2. 客户系统清单
## 3. 数据流图（ascii 或 mermaid）
## 4. 连接器规格
## 5. 认证与网络设计
## 6. 配置面
## 7. 风险登记
## 8. 实施分期（wave 1 / 2 / future）
## 9. 待澄清问题（供客户评审）
```

**不要立即构建**——本模块只产出设计。实现须在客户与内部利益相关方签字后开始。

<correct_patterns>

### 好的数据流规格

```
[WMS (on-prem, Oracle 19c)] → [nightly export job → CSV on SFTP] → [platform SFTP watcher] → [parse + validate] → [inventory_snapshots table]

Protocol:  SFTP (ssh-key auth, port 2222, client-side IP allowlist required)
Auth:      ED25519 keypair; client rotates annually, notifies 7 days ahead
Schema:    18 columns (sku, qty_on_hand, qty_reserved, location_code, ...)
           Validation: sku matches ^[A-Z]{3}\d{6}$; qty_on_hand >= 0
Cadence:   Nightly 02:00 client-local; file lands by 02:30; platform processes by 03:00
Error:     File missing by 03:00 → alert on-call; do NOT re-run client job unilaterally
```

**为什么好：** 每个字段都具体（端口 2222、ED25519、02:00 客户本地时间）；失败模式写明"不可做"（保护客户）；错误路径可执行。

### 好的连接器行

| 字段 | 值 |
|---|---|
| Name | `sftp-inventory-watcher` |
| Type | SFTP watcher（平台原生） |
| Language | 仅配置（无代码） |
| Effort | S（2h） |
| Reusability | 高——可参数化用于任意 SFTP CSV 投递 |

**为什么好：** 可复用性诚实打分（这条确实可产品化），工作量有量化，类型具体到能据此定工作量。

</correct_patterns>

<common_mistakes>

### 错误：模糊的数据流

```
"Inventory data will be transferred via SFTP. Auth will be configured by the client.
Errors will be handled appropriately."
```

**为什么坏：** 无协议细节、无认证细节、无失败语义。运维无法执行。

### 错误：占位认证

```
Auth: <TBD with client security team>
```

**为什么坏：** TBD 不是设计。要么给具体默认（如"ED25519 密钥对，客户提供公钥"），要么列 2-3 个选项带权衡。TBD 会随架构文档一起签发，然后变成"已批准的设计"。

### 应拒绝的合理化借口

- **"认证实现时再说，客户安全团队会告诉我们。"**
  → 现实：认证约束会重塑整个架构。晚到的"无外网"约束会让连接器选型作废。第 1 步就锁定。
- **"客户说 schema 稳定，不需要漂移检测。"**
  → 现实：客户对自己系统的断言是不可信数据。漂移检测是廉价保险；客户"我们从不改"的记忆不是。

</common_mistakes>

## 高频错误

1. 数据流用占位认证（`<TBD>`）
2. 连接器清单无复用性评分
3. 风险登记无缓解措施（只有风险）
4. 架构文档写"错误得到适当处理"
5. 无待澄清问题章节——假设当成事实

## 交付前检查

- [ ] 每条数据流五要素齐全（protocol + auth + schema + cadence + error）
- [ ] 每个连接器四字段齐全（type + language + effort + reusability）
- [ ] 每条风险都有缓解
- [ ] 无 `<TBD>` / `<fill-me>` 未配具体默认值
- [ ] 待澄清问题列出未知项
