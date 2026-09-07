# 部署手册 / Deployment Runbook

> 配套模块 / module: `references/06-deployment-runbook` ｜ ID：runbook- ｜ 本模板为骨架；模块 06 正文即"如何填写"的活样例。每次部署须带版本号（runbook-<client>-vX.Y）。

## 0. 飞行前 / Pre-flight
- [ ] 架构 + ADR 最新（`templates/adr.md`）
- [ ] Golden Set 达阈值（`templates/golden-set.csv` + `templates/eval-report.md`）
- [ ] 放权等级 L0–L3 与责任书面（授权人、范围、证据）
- [ ] 维护窗口已批 / 变更走廊可用

## 1. 版本与产物清单 / Version & artifacts
- 上版本→本版本 diff 涉及：镜像 / 迁移 / 配置 / flag（四类各注输入物路径）

## 2. 环境准备 / Environment
- 连通性（命令示例：`ping <host>`、探活端点 `curl https://<endpoint>/health`）
- 密钥与凭据（引用 secret-key-条目，绝对不含明文）

## 3.N 部署步骤示例 / Example deploy step
```bash
# Command
<可执行的完整命令，含预期输出>
# Expected output
<精确预期>
# If it fails
<症状 → 标准诊断动作，杜绝"换台机器试试">
```

## 4. 输入验证与可观测确认 / Validate & observe
- 金标准用例回放（抽取至少 1 个历史失败用例）
- 四件套确认：指标 / 结构化日志 / Trace / 审计（动作前后值可检索）
- 告警人工制造一次，记录触达耗时：__s

## 5. 回滚 / Rollback（五步）
停新版本 → 回滚 manifest → 迁移降级 → flag 恢复基线 → 健康检查返回上版本号

## 6. SLO 对照 / SLO
- 逐条对照 `templates/slo-table.md`；不安全动作 = 0 是硬否决

## 7. 记录与移交 / Record & handoff
- 审计：动作（ID、操作人、前后值、能否检索）
- 部署后 48h 值班要点；可复用修正标记 → 汇总到模块 09 retro
- 版本号：runbook-____ v____　日期：____