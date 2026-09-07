# 集成架构（节选）— arch-atlas-20260624（脱敏）

## 系统与组织清单（节选）
| 系统 | 部署 | 接口 | 数据 | 约束 |
|---|---|---|---|---|
| WMS Oracle19c | 本地 | 夜间作业→SFTP CSV | 库存快照 | ssh-key、端口 2222、IP 白名单 |
| OMS | 私有云 | REST(只读) | 工单 | 内网 OAuth2 client-credentials |
| TMS | SaaS(受控出网) | REST | 在途 | 代理白名单 |
| SOP 知识库 | 本地 | 同步进向量库 | 文档 | 版本化，失效标红 |

## 关键数据流
```
[WMS] → 02:00 导出 CSV → SFTP(2222, ED25519) → watcher → 校验 → inventory_snapshots
Schema：18 列；sku 正则 ^[A-Z]{3}\d{6}$；qty_on_hand>=0
失败：03:00 未见文件→告警值班；不得擅自重跑客户作业
```

## 连接器清单（节选）
| 连接器 | 类型 | 工作量 | 复用性 |
|---|---|---|---|
| sftp-inventory-watcher | 平台原生 SFTP watcher | S(2h) | 可产品化 |
| oms-readonly-client | REST 只读客户端 | M(1d) | 可参数化 |
| tms-proxy-adapter | 代理适配 | M(1d) | 一次性偏多 |

PoC 纵向切片仅启用 watcher + 知识库检索 + 分诊链路；OMS/TMS 适配器 wave 2。

## ADR-0007（节选）
- 背景：客户 WMS 历史上未通知改过列（访谈+既往事故）
- 候选：A 宽松自适应解析 / B 锁 schema v2 + 列数漂移即阻断并告警
- 决策：B（严格解析，漂移可见）
- 后果：新列需协同迁移；杜绝静默损坏
- 验证：Golden Set GS-014/GS-027、故障注入 FI-03

## 风险登记（节选）
| 风险 | 缓解 |
|---|---|
| schema 未通知变更 | 锁版本+漂移告警（ADR-0007） |
| 受控出网代理不稳 | TMS 失败时优雅降级为"在途未知，请人工核实" |
| 安全评审周期 | 提前交问卷与数据流图，预留 5 工作日 |
