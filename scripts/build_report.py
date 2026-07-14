#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""变化点管理（CPM）台账生成器：读取结构化数据，输出 Markdown + 纯文字版 TXT。
内置小样本（4 行），直接运行 `python build_report.py` 即可产出样例 MD+TXT。
产物默认写到当前工作目录（用户目录），不留在技能目录内。
"""
import argparse
import json
import os
import sys

# 内置小样本：4M1E 各一类（演示用，非真实数据）
SAMPLE = {
    "plant": "XX工厂 / 总装车间",
    "date": "2026-07-13",
    "owner": "李主管",
    "items": [
        {
            "no": "CPM-0713-01", "m4": "人", "content": "焊工甲顶岗（原焊工乙调休）",
            "risk": "中", "mark": "岗位标识牌+班前交底", "verify": "首件全检",
            "result": "合格", "owner": "张班长", "status": "已放行",
        },
        {
            "no": "CPM-0713-02", "m4": "料", "content": "密封圈启用新供应商批次",
            "risk": "高", "mark": "待验证区隔离", "verify": "首批 50 件追踪",
            "result": "待验证", "owner": "李QE", "status": "待验证",
        },
        {
            "no": "CPM-0713-03", "m4": "机", "content": "2号压装机大修后复产",
            "risk": "高", "mark": "设备点检合格牌", "verify": "Cpk 能力确认",
            "result": "Cpk=1.45 合格", "owner": "王PE", "status": "已放行",
        },
        {
            "no": "CPM-0713-04", "m4": "法", "content": "扭矩由 25±2 调为 28±2 N·m",
            "risk": "待补充", "mark": "待补充", "verify": "待补充",
            "result": "待补充", "owner": "待补充", "status": "待补充",
        },
    ],
}


def build_md(data):
    lines = []
    lines.append("# 变化点管理台账（CPM）\n")
    lines.append(f"**工厂/车间**：{data.get('plant','—')}")
    lines.append(f"**日期**：{data.get('date','—')}")
    lines.append(f"**台账主责**：{data.get('owner','—')}\n")
    lines.append("## 变化点明细\n")
    lines.append("| 追溯号 | 4M | 变化点内容 | 风险 | 标识 | 验证方案 | 验证结论 | 责任人 | 状态 |")
    lines.append("|--------|-----|------------|------|------|----------|----------|--------|------|")
    for it in data.get("items", []):
        lines.append(
            f"| {it.get('no','')} | {it.get('m4','')} | {it.get('content','')} | "
            f"{it.get('risk','待补充')} | {it.get('mark','')} | {it.get('verify','')} | "
            f"{it.get('result','')} | {it.get('owner','')} | {it.get('status','待补充')} |"
        )
    lines.append("")
    lines.append("## 说明\n")
    lines.append("- **风险**：高=客户/安全/法规或首用；中=参数微调/顶岗；低=等同替换。具体准则待企业补充。")
    lines.append("- **状态**：已放行=验证通过；待验证=禁止放行；跟踪中=跨班影响；待补充=信息缺失。")
    lines.append("")
    return "\n".join(lines)


def build_txt(data):
    lines = []
    lines.append("变化点管理台账（CPM）")
    lines.append("=" * 40)
    lines.append(f"工厂/车间：{data.get('plant','—')}")
    lines.append(f"日期：{data.get('date','—')}")
    lines.append(f"台账主责：{data.get('owner','—')}")
    lines.append("")
    lines.append("变化点明细")
    lines.append("-" * 40)
    for i, it in enumerate(data.get("items", []), 1):
        lines.append(f"【{i}】追溯号：{it.get('no','')}　4M：{it.get('m4','')}")
        lines.append(f"    变化点内容：{it.get('content','')}")
        lines.append(f"    风险：{it.get('risk','待补充')}　标识：{it.get('mark','')}")
        lines.append(f"    验证方案：{it.get('verify','')}　验证结论：{it.get('result','')}")
        lines.append(f"    责任人：{it.get('owner','')}　状态：{it.get('status','待补充')}")
        lines.append("")
    lines.append("说明")
    lines.append("-" * 40)
    lines.append("风险：高=客户/安全/法规或首用；中=参数微调/顶岗；低=等同替换（具体准则待企业补充）。")
    lines.append("状态：已放行=验证通过；待验证=禁止放行；跟踪中=跨班影响；待补充=信息缺失。")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", help="JSON 输入文件路径（缺省用内置小样本）")
    ap.add_argument("--out-dir", help="输出目录（缺省为当前工作目录）")
    ap.add_argument("--format", choices=["txt", "md", "all"], default="all",
                    help="输出格式：txt=纯文字版，md=Markdown，all=两者（默认）")
    a = ap.parse_args()

    if a.input:
        try:
            data = json.load(open(a.input, encoding="utf-8"))
        except Exception as e:
            print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
            sys.exit(1)
    else:
        data = SAMPLE

    out_dir = a.out_dir or os.getcwd()
    os.makedirs(out_dir, exist_ok=True)

    date_tag = data.get("date", "").replace("-", "") or "样例"
    base = f"变化点管理台账_{date_tag}"

    result = {"status": "success", "files": []}
    if a.format in ("md", "all"):
        md = build_md(data)
        md_path = os.path.join(out_dir, base + ".md")
        open(md_path, "w", encoding="utf-8").write(md)
        result["files"].append(md_path)
    if a.format in ("txt", "all"):
        txt = build_txt(data)
        txt_path = os.path.join(out_dir, base + ".txt")
        open(txt_path, "w", encoding="utf-8").write(txt)
        result["files"].append(txt_path)

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
