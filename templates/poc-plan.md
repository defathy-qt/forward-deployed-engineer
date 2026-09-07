# PoC 证明计划 / PoC Proof Plan

> 配套模块 / module: `references/04-evaluation` ｜ ID：POC- ｜ **先注册、后跑数 / register BEFORE running.**

## 关键业务假设 / Key business hypothesis
- 结果指标从基线 ___ 到目标 ___（围栏范围 ___）

## 最高风险假设（优先证伪）/ Highest-risk hypotheses
- H1：
- H2：

## 样本设计 / Sample design
- 样本量 / 时间窗 / 抽样方式（随机导出，禁止手挑易例）：
- 五层分层占比：正常 40% / 历史异常 25% / 边界模糊 15% / 缺失脏数据 10% / 对抗 10%

## 指标与通过条件（先验，三层独立）/ Metrics & pass conditions (pre-registered)
| 层 Layer | 指标 Metric | 通过阈值 Threshold | 分层下限 Floor per stratum |
|---|---|---|---|
| 结果 Result |  |  |  |
| 依据 Evidence | 伪造引用=0 |  |  |
| 动作 Action | 不安全动作=0（硬否决） |  |  |
| 业务 Business | vs 人工基线 |  |  |

## 失败/停止条件 / Fail & stop conditions
-

## 本 PoC 不做 / Out of PoC
- 压测、规模化、全量集成（属 Pilot/Production）

## 纵向切片 / Thin slice
- 真实输入→输出链路：接入→检索→推理→组织→引用→动作
- 打桩点（计为风险）：

## 签字（跑数前）/ Sign-off before run
业务 Owner：____ 技术 Owner：____ 日期：____
