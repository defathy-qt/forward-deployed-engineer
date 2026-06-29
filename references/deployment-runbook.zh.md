# 部署手册

**原则：** 需要判断或隐性知识的手册就是不完整。每一步明确到入职第一天的同事也能安全执行。

## 第 1 步：收集输入

| 输入 | 来源 |
|---|---|
| 集成架构 | `integration-architecture.zh.md` 产出 |
| 客户环境细节 | 调研记录、客户 IT 联系人 |
| 待部署平台版本 | 发布说明、变更日志 |
| 已知约束 | 隔离网络？仅 VPN？无外网？仅 Windows？ |
| 旧手册 | 版本控制 |
| 历史调试工件 | `client-debug.zh.md` 问题日志 |

## 第 2 步：手册模板

```markdown
# Deployment Runbook: <Client> — <Platform Version>

**Last updated:** YYYY-MM-DD
**Runbook version:** v<N>
**Owner:** <FDE name>
**Client contact:** <name, role, contact>

## 0. 飞行前检查
- [ ] 架构文档已评审且最新
- [ ] 客户环境访问已确认（VPN、SSH、dashboard）
- [ ] 所有前置已满足（见第 1 节）
- [ ] 维护窗口已批准
- [ ] 回滚计划已评审

## 1. 前置条件

### 1.1 客户侧
| Item | Requirement | How to verify | Owner |
|------|-------------|---------------|-------|
| ... | ... | ... | 客户 / FDE |

### 1.2 平台侧
| Item | Requirement | How to verify | Owner |
|------|-------------|---------------|-------|
| ... | ... | ... | FDE |

## 2. 环境准备

逐步来。确切命令，不要命令的描述。

### 2.1 网络与连通性
```bash
# 验证 VPN 连通性
ping <client_host>

# 验证外网访问（如适用）
curl -v https://<platform_endpoint>/health
```

### 2.2 密钥与配置
| Secret / Config | Value source | How to set | Rotate? |
|------------------|--------------|------------|---------|
| ... | 客户提供 | `export VAR=...` 或 vault 路径 | 每月 |

### 2.3 依赖
```bash
# 确切安装命令，锁定版本
```

## 3. 核心部署

按序逐步。每步写明：
- 确切命令或动作
- 期望输出或成功信号
- 失败模式与即时动作

### 3.N <步骤名>
```bash
# Command
<exact command>

# Expected output
<what success looks like>

# If it fails
<what to check first>
```

## 4. 验证

### 4.1 冒烟测试
| Test | Command | Expected |
|------|---------|----------|
| ... | ... | ... |

### 4.2 数据完整性检查
| Check | Query / command | Threshold |
|-------|------------------|-----------|
| ... | ... | ... |

## 5. 客户交接
- [ ] 客户联系人确认冒烟通过
- [ ] 客户联系人有 dashboard/监控访问
- [ ] 客户联系人知晓升级路径

## 6. 回滚

### 6.1 触发条件
- 何时回滚 vs 前向修复

### 6.2 步骤
```bash
# 回退到上一状态的确切命令
```

## 7. 部署后
- [ ] 手册已按实际偏差更新
- [ ] 若有问题已归档调试工件
- [ ] 若有平台缺口已归档反馈
```

## 第 3 步：健全性检查

交付前：

1. **每条命令可直接复制粘贴**——`<fill-me>` 必须配具体示例。
2. **每个条件分支明确**——"若 X 跳 3.2；若 Y 跳 6"。
3. **时间现实**——每节标注预计耗时，便于操作者规划。
4. **回滚真的有效**——脑中反向走一遍，能否恢复确切先前状态？

## 第 4 步：版本化与归档

- 提交到客户的部署仓库。
- 用平台版本与手册版本打 tag。
- 通知客户联系人与该客户其他 FDE。

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

### 好的回滚步骤

```bash
# 1. Stop the new version
kubectl scale deployment platform-api --replicas=0 -n prod

# 2. Re-apply previous manifest (includes the previous image, NOT the migration)
kubectl apply -f deploy/manifests/v4.8.1/ -n prod

# 3. Reverse the DB migration
kubectl exec -n prod deploy/platform-api -- python migrate.py downgrade v4.8.1

# 4. Verify
kubectl rollout status deployment/platform-api -n prod
# Expected: "deployment successfully rolled out"
curl -s https://api.atlas-logistics.example.com:8443/health
# Expected: {"status":"ok","version":"4.8.1"}
```

**为什么好：** 四步分明，每步可验证，按依赖顺序。镜像回退与迁移回退分开——因为它们是两件事。运维在任一步发现问题都可停下。

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

**为什么坏：** "troubleshoot" 不是动作。具体写：若 `kubectl rollout status` 显示 `ProgressDeadlineExceeded`，跳第 6 节（回滚）。若显示 `ImagePullBackOff`，查第 2.2 节镜像仓库凭证。

### 错误：不能恢复状态的回滚

```bash
# Rollback
kubectl rollout undo deployment/platform-api -n prod
```
但部署还跑了 DB 迁移时。

**为什么坏：** `rollout undo` 回退镜像但不回退迁移。回滚不完整——应用代码期望旧 schema，DB 是新 schema，调用失败。

### 错误："运维知道"

```bash
# Apply the usual network config
```

**为什么坏：** 没有"通常"。入职第一天没有通常。每条命令必须明确。"通常"是隐性知识——手册的存在是为了替代它，而非引用它。

### 应拒绝的合理化借口

- **"运维经验丰富，他们知道怎么做。"**
  → 现实：手册比个人长寿。老运维离职；新运维凌晨 3 点故障时继承这份文档。为第一天写。
- **"确切命令以后填，先把结构搭出来。"**
  → 现实：带占位符的结构和填好的手册一样容易直接交付。你现在不填，没人会填——下一位 FDE 会以为占位符意为"已稳定，勿动"。
- **"回滚就是部署的反向，不用写明。"**
  → 现实：部署含迁移、配置变更、外部状态（DNS、缓存、队列）。反向不对称。逐步写明，含迁移降级。

</common_mistakes>

## 高频错误

1. 占位符（`<fill-me>`）无具体示例
2. 模糊条件（"if it fails, troubleshoot"）
3. 回滚未覆盖 DB 迁移
4. 步骤无期望输出
5. 假设"运维知道"

## 交付前检查

- [ ] 每条命令可直接复制，无裸占位符
- [ ] 每步有期望输出
- [ ] 每个条件分支明确
- [ ] 回滚脑中反向走通，覆盖迁移
- [ ] 每节耗时现实
- [ ] 与执行运维过一遍
