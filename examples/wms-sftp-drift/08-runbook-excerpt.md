# 部署手册（节选）— runbook-atlas-v4.8.2（脱敏）

## 0. 飞行前
- [x] 架构+ADR-0007 最新；Golden Set v2 达阈值
- [x] 放权等级：R-01/R-02 = L2，其余 L1（运营总监书面）
- [x] 维护窗口 2026-08-10 02:00–04:00 已批

## 3.N 部署步骤示例
```bash
# Command
curl -v https://triage.internal.atlas.example:8443/health
# Expected output
< HTTP/2 200
< {"status":"ok","version":"4.8.2"}
# If it fails
# Connection refused → 查 2.1 跳板与内网 DNS；401 → 查 2.2 密钥轮换；404 → 对照架构第5节端点
```

## 4.3 可观测确认（2026-08-09 预发实测）
- 指标 14 序列在看板、30s 刷新（截图存档）
- 日志 correlation id 串起 ingest→retrieve→answer
- Trace 4 跳，P95 6.2s
- 审计：测试动作 AT-001 前后值可被合规检索
- 告警：14:22 人工制造 SLO 越线，48s 触达值班

## 故障注入（预发，五类全过）
数据冲突(GS-041 漂移阻断并告警) / 依赖失败(TMS 超时优雅降级) / 重复执行(幂等) /
版本异常(过期 SOP 不被采用) / 依据失效(被引文档删除→转人工)

## 7. 回滚（五步，已演练 2026-08-08）
停新版本 → 回滚 v4.8.1 manifest → 迁移降级 → flag 恢复基线 → 健康检查返回 4.8.1

## SLO（节选）
无纠正率≥97%（<95%/1h 呼叫）；不安全动作=0（任意一次呼叫并冻结放权）；P95≤8s
