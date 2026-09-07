# 端到端样例：Atlas 物流异常订单辅助分诊（全脱敏）

> 本目录用同一个虚构客户贯穿八阶段，展示工件如何环环相扣。公司、人员、数据均为
> 合成/脱敏；技术示例与 references 中的 SFTP 漂移案例呼应。阅读顺序即交付顺序。

## 背景（一句话）
物流公司夜间异常订单处理依赖人工跨 6 系统查单，4.5 人力、平均 38 分钟、退回率 11%；
FDE 交付"来源绑定的辅助分诊 Agent"，先围栏后放大，并把 SFTP 连接器沉淀为可复用资产。

## 工件链 / Artifact chain
| 阶段 | 文件 | 产出 ID |
|---|---|---|
| 1 发现 | 01-discovery-notes.md | DSC-atlas-20260620-01 |
| 1–2 相关者 | 02-stakeholder-map.md | STM-atlas-01 |
| 2 范围 | 03-scope-contract.md | SCP-atlas-v1 |
| 3–4 架构 | 04-integration-arch.md | arch-atlas-20260624 + ADR-0007 |
| 5 PoC/评测 | 05-poc-eval.md、06-golden-set.csv | POC-atlas-v1、EVAL-atlas-v1/v2 |
| 6 Pilot | 07-pilot-adoption.md | PLT-atlas-v1、UAT-atlas-v1 |
| 7 上线 | 08-runbook-excerpt.md、SLO | runbook-atlas-v4.8.2 |
| 8 事故→反馈→资产 | ISS-atlas-20260629-01.json、FB-2026-042.json、asset-manifest.yaml | ISS/FB/AM |

## 结果摘要（样例数值）
- 处理时长 38min → 4.1min（−89%），正确率 87.5% vs 人工 82%，不安全动作 0
- Pilot 两队列 L1→L2（仅 R-01/R-02），其余维持 L1
- 事故 ISS-01 催生平台级反馈 FB-042 与可复用资产 connector-sftp-watcher v1.2.0

## 关键教学点
1. 客户原话"做个问答机器人"被还原为业务问题（跨系统等待+口径不一）。
2. 通过条件在跑数前注册；v1 评测异常层不达标，修订后 v2 才晋级。
3. 客户未通知改列导致事故：分类为 client-upstream，修复方向是"暴露漂移"而非"静默接受"。
4. 资产带走行业理解（固定计划 SFTP CSV 模式），不带任何客户数据（样本合成）。
