# 变化点管理（change-point-management）

面向生产主管与质量工程师的变化点管理（CPM, Change Point Management）技能。对 4M（人/机/料/法，扩展环）变化点进行识别—标识—验证—追溯，防止变更悄无声息引发批量不良。

## 适用岗位
- 生产主管 / 线长：变化点第一发现人与现场执行者。
- 质量工程师（QE）：评估风险等级、确认验证方案与首件/首批结果。
- 工艺工程师（PE）：对"法"类变更给出受控标准与验证准则。
- 制造 / 质量经理：通过台账掌握过程稳定性与风险敞口。

## 解决的核心痛点
- 变更"悄悄"发生、无人识别无标识，直接流入生产导致批量不良。
- 风险不分级，关键变化点未被重点验证。
- 变了却没做首件/首批确认，问题在客户端才暴露。
- 变化点无记录无编号，发生不良时无法快速定位是否由变更引起。

## 产出物
- `变化点管理台账_YYYYMMDD.txt`：纯文字版台账，适合即时查看/打印。
- `变化点管理台账_YYYYMMDD.md`：结构化 Markdown 台账。

## 快速开始
```bash
# 直接运行，使用内置小样本产出样例 TXT+MD（写到当前目录）
python scripts/build_report.py

# 或基于自有 JSON 数据生成
python scripts/build_report.py --input 你的数据.json --out-dir 你的目录

# 只生成纯文字版 / 只生成 Markdown
python scripts/build_report.py --format txt
python scripts/build_report.py --format md
```

## 台账字段
追溯号 / 4M / 变化点内容 / 风险 / 标识 / 验证方案 / 验证结论 / 责任人 / 状态。
状态取值：已放行 ｜ 待验证 ｜ 跟踪中 ｜ 待补充。

## 联动技能（纯提示）
- 变化引发当班异常：`qrqc-quick-response`
- 防错固化变更：`poka-yoke-design`
- 不合格品返工返修：`rework-repair-plan`
- 设计/工程变更（ECN）：企业 ECN/EC 系统（非本技能范围）

## 说明
- 所有文档为简体中文；风险分级为通用提示，企业具体准则「待企业补充」。
- 本技能只做现场受控记录与追溯，不替代 ECN 流程与现场验证结论。
