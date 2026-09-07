# 合并并集对照清单 / Merge Union Checklist（FDE-01 × FDE-02 → FDE-v2）

> 目的：证明合并 = **并集不失真**——FDE-01 与 FDE-02 每一份独有要点都在合并产物中留有落点；
> 任何删减/改名必须在此登记理由。配合 `scripts/check-align.py references --strict` 机械校验。
> 核对日期：2026-09-07（v2.0.0 校验日）。

## 规则 / Rule
1. 合并允许模块比两原版都长（"重叠但各写一端" → 直接并入）。
2. 覆盖 = 内容并集；结构性删减只有在重命名/重组时发生，且内容不丢。
3. 模块正文只引用 `templates/`（单一事实源）——模板迁移不是内容删减。

## 逐模块盘点 / Per-module trace

| 合并模块 | FDE-01 独有要点落点 | FDE-02 独有要点落点 | 删减/理由 |
|---|---|---|---|
| 01-discovery | 利益相关者地图、逐角色访谈表、现状五要素、问题/症状/假设三分 | 独篇 discovery、逐字原话、多源交叉验证、量化基线、"是否该用 AI"路由 | `discovery-scoping` 拆分 → 仅改名，内容按两端并入 |
| 02-scoping | 范围合同三类边界、围栏动作、数值化停止条件、升级路径、三维机会评分 | 做/暂不做/绝不自动承诺、RACI、最小端到端闭环、ROI 假设 | 拆分改名，理由同上 |
| 03-integration-architecture | 组织盘点、PoC 纵向切片标注、ADR、连接器四字段含复用性评分、风险登记 | 防腐层、业务本体层（对象/关系/动作/规则/权限）、身份→授权→人工授权门→审计、对抗威胁 | 无内容删减 |
| 04-evaluation | 先验注册、五层 Golden Set、结果/依据/动作三层打分、人工基线、三桶结论 | 四层验收一票否决、防泄漏、错误分类→根因→回归 | `poc-evaluation` 改名 → 仅改名 |
| 05-pilot-adoption | 四轴围栏、L0–L3 放权证据表、八项上线门禁、熔断、采用六杠杆、Land & Expand | 六边界围栏、按角色培训、行为四指标、反馈闭环标签路由 | 围栏四轴并入六轴（内容并集），无删减 |
| 06-deployment-runbook | 可观测四件套、SLO 表、五类故障注入、灰度治理、镜像+迁移+flag 回滚 | 术后“可复用修正标记 → retro”闭环 | 无删减；补 `templates/deployment-runbook.md` 骨架（新增） |
| 07-client-debug | AI 六层故障定位、Golden Set 回归、最小失败案例永久入库 | 主体一致 +「分类与行业无关」注解 | 合并两端，保留独立模块编号 |
| 08-product-feedback | 通用性三级、impact 四字段含资产杠杆 | 第 6 步「双向蒸馏 → retro 资产化」闭环 | 无删减 |
| 09-retro-assets | asset-reuse 四层分离、asset 六要件、七类资产、版本化 manifest、复用度量 | retro 承诺 vs 交付、杠杆 KPI、迁移清单、RETRO JSON | 两端重叠 >60% → 合成单模块（内容两端全并，仅模块编号迁移） |
| 10-airgap-deploy | 隔离分级、信创栈盘点、离线交付包、数据边界、受限运维、离线升级 | —（FDE-02 无） | 全量保留 |

## 横切资产 / Cross-cutting
- **SKILL.md 入口**：全新编写（两版无前端 agent 入口）——能力模型、八阶段映射、18 类工件 ID、
  7 条硬规则、门禁四出口、L0–L3、语言路由、模块路由。
- **16 模板**：FDE-01 全量迁移，字段与 ID 按新模块核对；`deployment-runbook.md` 为新增（模块 06 引用其骨架）。
- **样例**：`wms-sftp-drift` 全保留（引用改新模块号）；新增 `gl-recon-drift`（Iris Bank，金融，全八阶段，合成数据）。
- **行业画像**：manufacturing / finance / government 三份保留，模块组合引用改新编号（全删减=0）。
- **工具链**：check-align.py = FDE-02（围栏剥离/交叉引用/占位符卫生）+ FDE-01（anchor 序列/长度比/--json/--strict）合并，**功能为并集**。

## 校验证据 / Evidence（2026-09-07）
- `python scripts/check-align.py references --strict` → **10/10 对齐，exit 0，0 warning**
- 交叉引用全解析：模块间同版本 ref 全部带编号前缀；`templates/` 引用全部落到真实文件（17 个模板文件）
- 全仓 grep 旧名（`discovery-scoping`/`poc-evaluation`/`asset-reuse`）：仅 CHANGELOG 的历史描述提及（记录改名，非引用）
- 样例/行业/README/SKILL 无裸模块名残留

## 已记录的删减 / Trims（完整列表）
**None。** 合并为并集与改名；无内容性删减。若后序发现遗漏独有要点，在此补记理由并回迁。