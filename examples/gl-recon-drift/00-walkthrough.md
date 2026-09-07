# 示例二 · 全程走读 — GL 对账·调账预审（Iris Bank）

> 全脱敏·样本合成。虚构城商行 **Iris Bank**，月结对账场景。数据全部合成，与真实账务无关。
> companion: examples/wms-sftp-drift/（物流·异常订单分诊）。两个样例互联：**ISS 科目映射漂移 呼应 ISS SFTP 漂移**；`connector-sftp-watcher`（物流样例产出的既有资产）在本样例被直接复用，演示 1→N 闭环。

## 一段话看懂这个样例

客户一开始要的是"**对账机器人**"（自动把差异平掉）。FDE 把需求还原成真问题：

> 月结对账 **3 天**；每笔差异人工定位约 **40 分钟**；季末月账实/账账差异率 **11%**。

红线：**过账与调账不可逆，绝不让系统自动执行**。最终交付的是「**归因 + 调账建议草稿**」——机器负责"哪里对不上、为什么、改哪边"，**授权门永远在人工手里**。这是一个典型的"**新能力 + 高风险围栏**"部署：长期停在 L0/L1，L2 仅限低风险围栏。

## 场景设定

- **客户**：虚构城商行 Iris Bank（以下全为合成数据）
- **场景**：月结（month-end close）——每月初对上月末账务。跨 **6 套系统**：总账（核心系统）、子账（存贷款核算）、资金（头寸/清算）、计提（利息与减值），经 **ESB** 与 **文件交换平台** 交换对账文件
- **部署环境**：金融专区、信创栈、强堡垒机 → 全程伴随 **10-airgap-deploy**
- **方式**：系统只出「归因 + 建议草稿」，人工授权门 + 审计链

## 八阶段 × 文件对应

| 阶段 | 模块 | 本样例文件 | 关键件 |
|---|---|---|---|
| S1 理解 | 01-discovery | [01-discovery-notes.md](01-discovery-notes.md) | DSC-iris-20260804-01 |
| S2 界定 | 02-scoping | [02-stakeholder-map.md](02-stakeholder-map.md)、[03-scope-contract.md](03-scope-contract.md) | STM-iris-01、SCP-iris-v1 |
| S3-4 架构 | 03-integration-architecture | [04-integration-arch.md](04-integration-arch.md) | arch-iris-20260807、ADR-0011、AM-connector-sftp-watcher-v1.2.0（复用） |
| S5 评测 | 04-evaluation | [05-poc-eval.md](05-poc-eval.md)、[06-golden-set.csv](06-golden-set.csv) | POC-iris-v1、EVAL-iris-v1/v2、golden-set-iris-v2 |
| S6 试点 | 05-pilot-adoption | [07-pilot-adoption.md](07-pilot-adoption.md) | PLT-iris-v1、UAT-iris-v1、八项门禁 |
| S7 部署运维 | 06-deployment-runbook | [08-runbook-excerpt.md](08-runbook-excerpt.md) | runbook-iris-v1.0、SLO-iris |
| 运营 | 07-client-debug | （ISS 记录） | [ISS-iris-20260828-01.json](ISS-iris-20260828-01.json) |
| 反馈 | 08-product-feedback | （FB 记录） | [FB-2026-058.json](FB-2026-058.json) |
| 保留 | 09-retro-assets | （RETRO/AM 记录） | [asset-manifest.yaml](asset-manifest.yaml) |
| 伴随 | 10-airgap-deploy | runbook 内含 | 专区/信创/强堡垒机 |

> 每个样例不要求逐文件逐阶段铺开；本样例按"中心即边缘"取舍——重点在**归因质量（evaluation）**、**授权门（pilot）**与**审计链（runbook）**，排障与反馈以 JSON 记录示形。

## 教学点（沿 8 阶段）

1. **S1 需求还原**（01-discovery）：客户嘴里的"对账机器人" → 用「问题/症状/假设」三分揪出真问题。真基线是**时长与差异率**，不是"有没有机器人"。
2. **S2 边界**（03-scope-contract）：**绝不自动承诺**——"过账/调账自动执行"一开始就划在边界之外；围栏动作只到「草稿」。
3. **S3 架构**（04-integration-arch）：身份→授权→**人工授权门**→审计链；业务本体层定义"科目映射"这张表的**对象/关系/规则/权限**——为 ISS 的科目映射漂移埋线。
4. **S5 评测**（04-evaluation → 05-poc-eval + golden set）：五层 Golden Set，**依据层**引入"科目映射引用必须可回溯到当天有效表快照"；越权提取客户户名余额 = 对抗用例。
5. **S6 试点**（05-pilot-adoption）：放权 L0/L1 长期停留；UAT 用**4 类脚本**覆盖 正常/异常/拒绝升级/依据接管；8 月月结作为**险情窗口**提前演练，09-05 硬决策。
6. **S7 部署运维**（06-deployment-runbook）：审计事件（调账草稿的 full审计链）、强堡垒机、SLO（定位时长/无纠正率/不安全动作=0）。
7. **1→N 复用**（贯穿）：ISS 科目映射漂移 → FB-2026-058 平台级反馈；`connector-sftp-watcher`（来自物流样例）原样复用承载文件落地 → 一次沉淀、N 处受益。

## 已确认的决策（本样例时点）

- 真问题 =「月结对账 3 天 / 单笔差异定位 40 分钟 / 季末差异率 11%」，不是"要个机器人"。
- 系统顶部动作 =「归因 + 调账建议草稿」；过账/调账执行永远留人工（授权门 + 审计链）。
- 科目映射表（subject-mapping）**授信接入**，锁表 + 漂移检测（呼应物流样例 SFTP 漂移）。
- 放权：L0 先跑 10 天，L1 长驻；L2 仅限"低风险围栏"（自动回填草稿的归因理由，不可自动过账）。
- 信创/专区/强堡垒机从 S3 起就是架构输入，**不是后补**。

## 用到的工件 ID

DSC- / STM- / SCP- / arch- / ADR- / POC- / EVAL- / golden-set- / PLT- / UAT- / runbook- / SLO- / ISS- / FB- / RETRO- / AM- ——完整 ID 表见 SKILL.md。