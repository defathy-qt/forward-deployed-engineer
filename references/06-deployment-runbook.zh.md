# 部署手册

**目标：** 需要判断或隐性知识的手册就是不完整。每一步明确到**入职第一天的同事**也能安全执行——包括可观测性、故障演练和可回退的变更路径。

> 部署不是把代码推上去就算完——而是交付"有人能观测、有人能接管、有人能回滚"的运行状态。回滚包含镜像、迁移、配置与 flag 四件事，反向不对称。

## 输入与输出

| | |
|---|---|
| 输入 | `arch-<client-slug>-<YYYYMMDD>.md` 架构与全部 ADR、`EVAL-<client>-vN` 评测报告与冻结 Golden Set、`PLT-<client>-vN` Pilot 计划与 `UAT-<client>-vN`/已批准放权等级、客户环境细节与 IT 联系人、待部署平台版本、已知约束（隔离网络？仅 VPN？无外网？仅 Windows？）、旧手册、历史调试工件 |
| 输出 | `runbook-<client>-vN` 部署手册、`SLO-<client>-vN` SLO 表、`PM-<client>-vN` postmortem、部署后修订标记 |
| 下游 | `07-client-debug.md`（问题日志与排障）、`09-retro-assets.md`（可复用修正闭环）、`08-product-feedback.md`（平台缺口反馈） |

## 第 1 步：收集输入 <!--a:step1-->

| 输入 | 来源 |
|---|---|
| 集成架构 | `03-integration-architecture.md` 产出 + 全部 ADR |
| 评测报告与 Golden Set | `04-evaluation.md` 产出；待复验的通过条件 |
| Pilot 计划与 UAT 记录 | `05-pilot-adoption.md` 产出；已批准的放权等级 |
| 客户环境细节 | 调研记录（`01-discovery.md`）、客户 IT 联系人 |
| 待部署平台版本 | 发布说明、变更日志 |
| 已知约束 | 隔离网络？仅 VPN？无外网？仅 Windows？ |
| 旧手册 | 版本控制（对比增量） |
| 历史调试工件 | `07-client-debug.md` 问题日志 |

## 第 2 步：手册模板 <!--a:step2-->

```markdown
# Deployment Runbook: <Client> — <Platform Version>

**Last updated:** YYYY-MM-DD
**Runbook version:** v<N>
**Owner:** <FDE name>
**Client contact:** <name, role, contact>
**Approved autonomy level:** shadow | assist | limited-auto | full-auto

## 0. 飞行前检查
- [ ] 架构文档与 ADR 已评审且最新
- [ ] 冻结 Golden Set 上的评测通过条件已复验
- [ ] 客户环境访问已确认（VPN、SSH、dashboard）
- [ ] 所有前置已满足（见第 1 节）
- [ ] 维护窗口已批准；回滚计划已评审

## 1. 前置条件
### 1.1 客户侧
| Item | Requirement | How to verify | Owner |
|------|-------------|---------------|-------|
| ... | ... | ... | 客户 / FDE |
### 1.2 平台侧
| Item | Requirement | How to verify | Owner |
|------|-------------|---------------|-------|

## 2. 环境准备
### 2.1 网络与连通性
# 验证 VPN 连通性
ping <client_host>
# 验证外网访问（如适用）
curl -v https://<platform_endpoint>/health
### 2.2 密钥与配置
| Secret / Config | Value source | How to set | Rotate? |
|------------------|--------------|------------|---------|
| ... | 客户提供 | `export VAR=...` 或 vault 路径 | 每月 |
### 2.3 依赖
# 确切安装命令，锁定版本（隔离网络用离线包，见 10-airgap-deploy.md）

## 3. 核心部署
逐步执行。每步写明：
- 确切命令或动作
- 期望输出或成功信号
- 失败模式与即时动作

### 3.N <步骤名>
# Command
<exact command>
# Expected output
<what success looks like>
# If it fails
<what to check first>

## 4. 验证
### 4.1 冒烟测试       | Test | Command | Expected |
### 4.2 数据完整性检查 | Check | Query / command | Threshold |
### 4.3 可观测性确认   指标、结构化日志、Trace、审计事件全部在流；SLO 看板已上线

## 5. 灰度/分批发布
队列顺序、晋级条件、暂停/回滚触发线（见第 4 步）。

## 6. 客户交接
- [ ] 客户联系人确认冒烟通过
- [ ] 客户联系人有 dashboard/监控访问
- [ ] 客户联系人知晓升级路径
- [ ] 放权等级及其边界已书面说明

## 7. 回滚
触发条件；确切步骤，含迁移降级、配置回退与 flag 恢复（见第 4 步）。

## 8. 部署后
- [ ] 手册已按实际偏差更新
- [ ] 新调试工件已归档；新 Golden Set 回归已补（见 07-client-debug.md）
- [ ] 需要时已归档产品反馈/资产提案
- [ ] 可复用修正已标记进 09-retro-assets.md——让下一份手册起点更高
```

## 第 3 步：可观测最小集与 SLO <!--a:step3-->

上线前四类信号必须全部在线——**无法观测的 AI 系统就无法安全自动化**：

| 信号 | 最小内容 |
|---|---|
| 指标 | 请求量、时延、错误率、人工接管率、token/成本 |
| 结构化日志 | 全链路同一 correlation id；输入类别、决策、输出 |
| Trace | 检索→模型→工具→动作各跳耗时 |
| 审计事件 | 谁/什么对什么数据执行了什么动作，前后值（可检索、防篡改） |

与客户共同定义一张小 SLO 表（模板：`templates/slo-table.md`）；**每个 SLO 都要有告警和 Owner**：

```
SLI：无需人工纠正完成的辅助分诊占比
SLO：滚动 7 天 ≥97%          告警：连续 1h <95% → 呼叫值班
SLI：不安全动作数            SLO：0                    告警：出现任意一次 → 呼叫并冻结放权
SLI：端到端 P95 时延         SLO：≤8s                  告警：连续 15min >12s
```

## 第 4 步：故障注入与变更治理 <!--a:step4-->

**在客户遇到故障之前先演练。** 预发至少注入五类故障并记录系统表现：数据冲突（schema 漂移/重复键）、依赖失败（下游超时/宕机）、重复执行（重试/重复提交）、审批/版本异常（SOP 过期、模型版本错误）、依据失效（被引文档被删/过期）。每类都必须**安全降级或告警——绝不静默产出**。

生产变更治理：

1. **灰度/分批**——最小队列先上；SLO 守住才晋级（队列顺序与触发线写入手册第 5 节）。
2. **晋级条件事前写明**——指标与时间窗，不凭感觉。
3. **暂停与回滚触发线数值化**——回滚同时覆盖**镜像、数据迁移、配置与 feature flag** 四件事。
4. **每起事故做 Postmortem**（模板：`templates/postmortem.md`）→ 一个修复、一次手册更新、一条新 Golden Set 回归（见 `07-client-debug.md`）。

### 部署四出口决策记录

每一次分批晋级都是一次门禁，用与评测一致的四出口词汇决策并记录证据：

| 出口 | 条件 | 动作 |
|---|---|---|
| **继续** | 当前批次 SLO 达标、无新崩溃 | 晋级下一批 |
| **收窄** | 部分维度达标但风险偏高 | 保持当前规模，暂停扩批 |
| **修订** | 方向成立、某类故障可前向修复 | 修复后从当前批次重新晋级（不跳过） |
| **停止（回滚）** | SLO 越线触发回滚线 | 执行第 7 节回滚，回到可验证的先前状态 |

```markdown
# 部署四出口决策记录：<客户> — <发布 vN> <日期>
- 出口：<继续 / 收窄 / 修订 / 停止-回滚>
- 依据：<本批 SLO 数字、告警次数、故障注入/真实故障观察>
- 决策人：<具名；回滚决策无需审批，值班可立即执行>
```

## 第 5 步：健全性检查 <!--a:step5-->

交付前：

1. **每条命令可直接复制粘贴**——`<fill-me>` 必须配具体示例。
2. **每个条件分支明确**——"若 X 跳第 3.2 节；若 Y 跳第 7 节"，不写"排障并重试"。
3. **时间现实**——每节标注预计耗时，便于操作者规划。
4. **回滚真的有效**——脑中反向走一遍：镜像、迁移、配置、flag 四件事能否逐一恢复确切先前状态？
5. **可观测与 SLO 告警要被证实能触发**，而不只是配置了。

## 第 6 步：版本化与归档 <!--a:step6-->

- 提交到客户的部署仓库。
- 用平台版本与手册版本打 tag。
- 通知客户联系人与该客户其他 FDE。
- 把**可复用修正**标记进 `09-retro-assets.md`、系统性缺口写入 `08-product-feedback.md`，让下一份手册起点更高（FDE-02 闭环）。

## 模板 / 工件 <!--a:template-->

- `templates/deployment-runbook.md`（若单独放置）——手册骨架；本模块正文即模板
- `templates/slo-table.md` —— SLO 表
- `templates/postmortem.md` —— 事故复盘
- 产出 ID：`runbook-<client>-vN`、`SLO-<client>-vN`、`PM-<client>-vN`

**门禁提示：** 无四类信号、无 SLO 告警证实触发、无五类故障注入演练、无覆盖镜像+迁移+配置+flag 的回滚演练 → 不得部署生产。占位符手册同样是"已批准的设计"。

<correct_patterns>

### 好的步骤块

```bash
# Command
curl -v https://api.atlas-logistics.example.com:8443/health

# Expected output
< HTTP/2 200
< {"status":"ok","version":"4.8.2"}

# If it fails
# — Connection refused → check VPN (Section 2.1)
# — 401              → check secret rotation (Section 2.2)
# — 404              → wrong endpoint, verify against arch doc Section 5
```

**为什么好：** 命令可直接复制（真实 host、真实端口）；期望输出精确（状态码 + body 形态）；失败模式交叉引用其他章节，运维不会卡住。

### 好的回滚步骤（镜像 + 迁移 + flag 分离）

```bash
# 1. Stop the new version
kubectl scale deployment platform-api --replicas=0 -n prod
# 2. Re-apply previous manifest (includes the previous image, NOT the migration)
kubectl apply -f deploy/manifests/v4.8.1/ -n prod
# 3. Reverse the DB migration
kubectl exec -n prod deploy/platform-api -- python migrate.py downgrade v4.8.1
# 4. Reset feature flags to previous baseline
kubectl exec -n prod deploy/platform-api -- python flags.py restore v4.8.1
# 5. Verify
kubectl rollout status deployment/platform-api -n prod
curl -s https://api.atlas-logistics.example.com:8443/health
# Expected: {"status":"ok","version":"4.8.1"}
```

**为什么好：** 五步分明，每步可验证，按依赖顺序。镜像、迁移、flag 是分开的独立动作——回滚不对称，必须逐件写明，运维在任一步发现问题都可停下。

### 好的可观测性确认

```
2026-07-14 预发环境确认：
- 指标：   看板可见 14 条序列，30s 刷新（附截图）
- 日志：   correlation id 8c2... 把 ingest→retrieve→answer 6 行串起
- Trace：  可见 4 跳，P95 6.2s
- 审计：   测试动作 AT-001 写入前后值记录，合规可检索
- 告警：   14:22 人工制造 SLO 越线；48s 内呼叫到值班
```

**为什么好：** 可观测性靠"主动制造一次故障"来证明，而非假设配置即生效；每个信号都有证据和时间戳。

</correct_patterns>

<common_mistakes>

### 错误：占位符无示例

```bash
curl https://<client_host>:<port>/health
```

**为什么坏：** 运维不知道合法 host/port 长什么样。每个占位符配具体示例：`curl https://api.atlas-logistics.example.com:8443/health`。

### 错误：模糊条件

```
"If the deployment fails, troubleshoot and retry."
```

**为什么坏：** "troubleshoot" 不是动作。具体写：若 `kubectl rollout status` 显示 `ProgressDeadlineExceeded`，跳第 7 节（回滚）。若显示 `ImagePullBackOff`，查第 2.2 节镜像仓库凭证。

### 错误：不能恢复状态的回滚

```bash
kubectl rollout undo deployment/platform-api -n prod
```
但部署还跑了 DB 迁移并切换了 feature flag 时。

**为什么坏：** `rollout undo` 只回退镜像。应用代码期望旧 schema 与旧 flag——调用会以难以诊断的方式失败。回滚必须覆盖镜像 + 迁移 + 配置 + flag。

### 错误："运维知道"

```bash
# Apply the usual network config
```

**为什么坏：** 没有"通常"。入职第一天没有通常。每条命令必须明确。"通常"是隐性知识——手册的存在是为了替代它，而非引用它。

### 应拒绝的合理化借口

- **"运维经验丰富，他们知道怎么做。"**
  → 现实：手册比个人长寿。老运维离职；新运维凌晨 3 点故障时继承这份文档。为第一天写。
- **"第一次上线就做故障注入太夸张了。"**
  → 现实：这五类故障正是生产最先交付的东西。预发演练是几小时，生产排查是几天加信任损失。
- **"确切命令以后填，先把结构搭出来。"**
  → 现实：带占位符的结构和填好的手册一样容易直接交付。你现在不填，没人会填。
- **"回滚就是部署的反向，不用写明。"**
  → 现实：部署含迁移、flag、外部状态（DNS、缓存、队列）。反向不对称。逐步写明。

</common_mistakes>

## 高频错误 <!--a:top-->

1. 占位符（`<fill-me>`）无具体示例
2. 模糊条件（"if it fails, troubleshoot"）
3. 回滚漏了迁移/flag/配置回退
4. 步骤无期望输出
5. 可观测只配置未证实能触发
6. 五类故障未演练
7. 假设"运维知道"
8. 术后未回传可复用修正（目录越积越矮）

## 交付前检查 <!--a:checklist-->

- [ ] 每条命令可直接复制，无裸占位符
- [ ] 每步有期望输出
- [ ] 每个条件分支明确（含"若失败跳哪节"）
- [ ] 回滚脑中反向走通，覆盖镜像 + 迁移 + 配置 + flag
- [ ] 四类可观测信号在线；SLO 告警已证实触发
- [ ] 五类故障注入已演练并记录结果
- [ ] 灰度晋级/暂停/回滚触发线数值化且事前达成一致
- [ ] 每节耗时现实；已与执行运维过一遍
- [ ] 术后：手册已更新、调试工件已归档、可复用修正已标记进 09、缺口已写入 08