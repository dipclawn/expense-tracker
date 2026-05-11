#!/usr/bin/env python3
"""
Expense Tracker v2.0 - 极简命令行记账工具
数据存储在 ~/.expense-tracker/data.json
"""

import json
import os
import sys
import csv
from datetime import datetime, date, timedelta
from collections import defaultdict

DATA_DIR = os.path.expanduser("~/.expense-tracker")
DATA_FILE = os.path.join(DATA_DIR, "data.json")

CATEGORIES = {
    "expense": ["餐饮", "交通", "购物", "娱乐", "住房", "医疗", "教育", "日用", "服饰", "其他"],
    "income":  ["工资", "兼职", "红包", "投资", "理财", "退款", "其他"],
}


def ensure_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"records": [], "budgets": {}}, f, ensure_ascii=False, indent=2)


def load():
    ensure_data()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    ensure_data()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def next_id(records):
    return max((r["id"] for r in records), default=0) + 1


# ====== 命令函数 ======

def cmd_add(args):
    """记一笔"""
    data = load()
    record = {
        "id": next_id(data["records"]),
        "type": args.get("type", "expense"),
        "amount": float(args["amount"]),
        "category": args["category"],
        "note": args.get("note", ""),
        "date": args.get("date", datetime.now().strftime("%Y-%m-%d %H:%M")),
        "timestamp": datetime.now().isoformat(),
    }
    data["records"].append(record)
    save(data)
    symbol = "📤" if record["type"] == "income" else "💸"
    sign = "+" if record["type"] == "income" else "-"
    print(f"{symbol} 已记录 #{record['id']}: {record['category']} {sign}¥{record['amount']:.2f} {record['note']}")


def cmd_list(args):
    """列出账单"""
    data = load()
    records = data["records"]
    if not records:
        print("📭 暂无记账记录")
        return

    # 过滤
    days = args.get("days")
    ttype = args.get("type")
    cat = args.get("category")
    today = date.today()

    if days:
        try:
            days = int(days)
        except (ValueError, TypeError):
            days = None
    if days:
        cutoff = today - timedelta(days=days)
        records = [r for r in records if datetime.strptime(r["date"][:10], "%Y-%m-%d").date() >= cutoff]
    if ttype:
        records = [r for r in records if r["type"] == ttype]
    if cat:
        records = [r for r in records if r["category"] == cat]

    if not records:
        print("📭 没有符合条件的记录")
        return

    # 统计小计
    income_sum = sum(r["amount"] for r in records if r["type"] == "income")
    expense_sum = sum(r["amount"] for r in records if r["type"] == "expense")

    print(f"\n{'='*58}")
    period = f"最近{days}天" if days else "全部"
    print(f"📋 {period} 共{len(records)}条  收入¥{income_sum:.0f}  支出¥{expense_sum:.0f}")
    print(f"{'='*58}")
    for r in reversed(records[-50:]):
        symbol = "📤" if r["type"] == "income" else "💸"
        sign = "+" if r["type"] == "income" else "-"
        d = r["date"][:16] if len(r["date"]) >= 16 else r["date"]
        note = f"  {r['note']}" if r.get("note") else ""
        print(f"  #{r['id']:>3} {d} {symbol} {r['category']:>4} {sign}¥{r['amount']:>8.2f}{note}")
    print(f"{'='*58}\n")


def cmd_summary(args):
    """统计"""
    data = load()
    records = data["records"]
    if not records:
        print("📭 暂无数据")
        return

    today = date.today()
    month = args.get("month", today.month)
    year = args.get("year", today.year)

    # 筛选月份
    monthly = [r for r in records
               if datetime.strptime(r["date"][:10], "%Y-%m-%d").year == year
               and datetime.strptime(r["date"][:10], "%Y-%m-%d").month == month]

    if not monthly:
        print(f"📭 {year}年{month}月 无记录")
        return

    income = sum(r["amount"] for r in monthly if r["type"] == "income")
    expense = sum(r["amount"] for r in monthly if r["type"] == "expense")

    print(f"\n{'='*45}")
    print(f"📊 {year}年{month}月 财务报告")
    print(f"{'='*45}")
    print(f"  📤 收入: ¥{income:>10.2f}")
    print(f"  💸 支出: ¥{expense:>10.2f}")
    print(f"  💰 结余: ¥{income - expense:>10.2f}")
    print(f"  📋 笔数: {len(monthly)}")

    # 支出分类
    expense_cats = defaultdict(float)
    for r in monthly:
        if r["type"] == "expense":
            expense_cats[r["category"]] += r["amount"]

    if expense_cats:
        print(f"\n  📊 支出分布:")
        for cat, amt in sorted(expense_cats.items(), key=lambda x: -x[1]):
            pct = amt / expense * 100 if expense else 0
            bar = "█" * max(1, int(pct // 4))
            print(f"    {cat:>4}  ¥{amt:>8.2f}  {pct:>5.1f}%  {bar}")

    # 预算对比
    budgets = data.get("budgets", {})
    if budgets:
        print(f"\n  🎯 预算对比:")
        for cat, budget in budgets.items():
            spent = expense_cats.get(cat, 0)
            remain = budget - spent
            pct = spent / budget * 100 if budget else 0
            flag = "⚠️" if pct > 80 else "✅" if pct <= 100 else "❌"
            bar = "▓" * min(20, int(pct // 5)) + "░" * max(0, 20 - min(20, int(pct // 5)))
            print(f"    {cat:>4}  ¥{spent:>7.2f}/{budget:<7.2f}  {bar} {pct:.0f}% {flag}")

    print(f"{'='*45}\n")


def cmd_budget(args):
    """设置预算"""
    data = load()
    cat = args["category"]
    amount = float(args["amount"])
    data.setdefault("budgets", {})[cat] = amount
    save(data)
    print(f"🎯 已设置 {cat} 月度预算: ¥{amount:.2f}")


def cmd_export(args):
    """导出CSV"""
    data = load()
    path = args.get("path", os.path.join(DATA_DIR, "export.csv"))
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "类型", "金额", "分类", "备注", "日期"])
        for r in data["records"]:
            t = "收入" if r["type"] == "income" else "支出"
            writer.writerow([r["id"], t, r["amount"], r["category"], r["note"], r["date"]])
    print(f"📤 已导出 {len(data['records'])} 条记录 → {path}")


def cmd_delete(args):
    """删除记录"""
    data = load()
    rid = int(args["id"])
    before = len(data["records"])
    data["records"] = [r for r in data["records"] if r["id"] != rid]
    if len(data["records"]) < before:
        save(data)
        print(f"🗑️ 已删除记录 #{rid}")
    else:
        print(f"❌ 未找到记录 #{rid}")


def cmd_edit(args):
    """编辑记录"""
    data = load()
    rid = int(args["id"])
    for i, r in enumerate(data["records"]):
        if r["id"] == rid:
            if "amount" in args:
                data["records"][i]["amount"] = float(args["amount"])
            if "category" in args:
                data["records"][i]["category"] = args["category"]
            if "note" in args:
                data["records"][i]["note"] = args["note"]
            save(data)
            print(f"✏️ 已更新记录 #{rid}")
            return
    print(f"❌ 未找到记录 #{rid}")


def cmd_categories():
    print("\n📂 支出分类:", ", ".join(CATEGORIES["expense"]))
    print("📂 收入分类:", ", ".join(CATEGORIES["income"]))
    print("💡 分类可自由添加，不受限\n")


def cmd_help():
    print("""
💰 Expense Tracker v2.0 - 极简记账工具

用法:
  add    python3 expense.py add -a <金额> -c <分类> [-n 备注] [-t income] [-d 日期]
  list   python3 expense.py list [--days N] [--type income|expense] [--category 分类]
  sum    python3 expense.py summary [--month M] [--year Y]
  budget python3 expense.py budget -c <分类> -a <预算金额>
  export python3 expense.py export [-p 路径]
  del    python3 expense.py del <ID>
  edit   python3 expense.py edit <ID> [-a 金额] [-c 分类] [-n 备注]
  cat    python3 expense.py categories

示例:
  python3 expense.py add -a 25 -c 餐饮 -n "午饭"
  python3 expense.py add -a 5000 -c 工资 -t income
  python3 expense.py add -a 128 -c 购物 -n "买书" -d "2026-05-10"
  python3 expense.py list --days 7
  python3 expense.py summary --month 5
  python3 expense.py budget -c 餐饮 -a 2000
  python3 expense.py export -p ~/Desktop/账单.csv
""")


# ====== 参数解析 ======

def parse_args():
    """简陋但够用的参数解析"""
    if len(sys.argv) < 2:
        cmd_help()
        sys.exit(0)

    cmd = sys.argv[1]
    args = {}
    i = 2

    while i < len(sys.argv):
        if sys.argv[i].startswith("--"):
            key = sys.argv[i][2:]
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("-"):
                args[key] = sys.argv[i + 1]
                i += 2
            else:
                args[key] = True
                i += 1
        elif sys.argv[i].startswith("-") and len(sys.argv[i]) == 2:
            key = {"a": "amount", "c": "category", "n": "note", "t": "type",
                   "d": "date", "p": "path", "m": "month", "y": "year"}.get(sys.argv[i][1])
            if key and i + 1 < len(sys.argv):
                args[key] = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        else:
            # 位置参数: delete <id> / edit <id>
            if cmd in ("delete", "del", "edit") and "id" not in args:
                args["id"] = sys.argv[i]
            i += 1

    return cmd, args


# ====== 主程序 ======

COMMANDS = {
    "add": cmd_add, "a": cmd_add,
    "list": cmd_list, "ls": cmd_list, "l": cmd_list,
    "summary": cmd_summary, "sum": cmd_summary, "s": cmd_summary,
    "budget": cmd_budget,
    "export": cmd_export,
    "delete": cmd_delete, "del": cmd_delete,
    "edit": cmd_edit,
    "categories": cmd_categories, "cat": cmd_categories,
    "help": cmd_help, "--help": cmd_help, "-h": cmd_help,
}

if __name__ == "__main__":
    cmd, args = parse_args()
    if cmd in COMMANDS:
        COMMANDS[cmd](args)
    else:
        print(f"❌ 未知命令: {cmd}")
        cmd_help()
