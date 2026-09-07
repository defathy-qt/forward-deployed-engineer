# SLO 表 / Service Level Objective Table

> 配套模块 / module: `references/06-deployment-runbook` ｜ ID：SLO- ｜ 每个 SLO 必须有告警与 Owner / every SLO needs an alert and an owner.

| SLI（指标定义） | SLO 目标 | 统计窗口 | 告警阈值 | 告警动作 | Owner |
|---|---|---|---|---|---|
| 无人工纠正完成率 | ≥97% | 滚动 7 天 | 连续 1h <95% | 呼叫值班 |  |
| 不安全动作数 | 0 | 实时 | 出现任意 1 次 | 呼叫+冻结放权 |  |
| 端到端 P95 时延 | ≤8s | 滚动 1h | 连续 15min >12s | 值班排查 |  |
| 人工接管率 | ≤20% | 滚动 7 天 | >35% | 复盘是否退化 |  |
| 引用可溯率 | ≥99% | 滚动 7 天 | <97% | 检查知识库 |  |

## 可观测四件套确认 / Four signals live
- [ ] 指标 Metrics（看板序列数、刷新频率、截图）
- [ ] 结构化日志 Logs（全链路 correlation id）
- [ ] Trace（各跳耗时）
- [ ] 审计 Audit（动作前后值、可被合规检索）
- [ ] 告警触发已人工制造一次并证实触达（时间：__，触达耗时：__）
