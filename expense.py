#!/usr/bin/env python3
"""
Expense Tracker - 极简命令行记账工具
数据存储在 ~/.expense-tracker/data.json
"""

import json
import os
import sys
from datetime import datetime, date
from collections import defaultdict

DATA_DIR = os.path.expanduser("~/.expense-tracker")
DATA_FILE = os.path.join(DATA_DIR, "data.json")

CATEGORIES_EXPENSE = ["餐饮", "交通", "购物", "娱乐", "住房", "医疗", "教育", "其他"]
CATEGORIES_INCOME = ["工资", "兼职", "红包", "投资", "其他"]


def ensure_data():
    """确保数据文件和目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"records": []}, f, ensure_ascii=False, indent=2)


def load_records():
    """加载所有记录"""
    ensure_data()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["records"]


def save_records(records):
    """保存记录"""
    ensure_data()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"records": records}, f, ensure_ascii=False, indent=2)


def add_record(amount, category, note="", ttype="expense"):
    """添加一条记录"""
    records = load_records()
    record = {
        "id": len(records) + 1,
        "type": ttype,
        "amount": amount,
        "category": category,
        "note": note,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "timestamp": datetime.now().isoformat(),
    }
    records.append(record)
    save_records(records)
    symbol = "📤" if ttype == "income" else "💸"
    print(f"{symbol} 已记录: {category} {'+' if ttype == 'income' else '-'}¥{amount:.2f} {note}")
    return record


def list_records(days=None, ttype=None):
    """列出账单"""
    records = load_records()
    if not records:
        print("📭 暂无记账记录")
        return

    today = date.today()
    if days:
        records = [r for r in records if (today - datetime.strptime(r["date"][:10], "%Y-%m-%d").date()).days <= days]
    if ttype:
        records = [r for r in records if r["type"] == ttype]

    if not records:
        print("📭 没有符合条件的记录")
        return

    print(f"\n{'='*50}")
    print(f"📋 共 {len(records)} 条记录")
    print(f"{'='*50}")
    for r in reversed(records[-30:]):  # 最多显示30条
        symbol = "📤" if r["type"] == "income" else "💸"
        sign = "+" if r["type"] == "income" else "-"
        print(f"  #{r['id']:>3} {r['date']} {symbol} {r['category']:>4}  {sign}¥{r['amount']:>8.2f}  {r['note']}")
    print(f"{'='*50}\n")


def summary(month=None, year=None):
    """月度/年度统计"""
    records = load_records()
    if not records:
        print("📭 暂无数据")
        return

    today = date.today()
    month = month or today.month
    year = year or today.year

    filtered = []
    for r in records:
        d = datetime.strptime(r["date"][:10], "%Y-%m-%d")
        if d.year == year and d.month == month:
            filtered.append(r)

    if not filtered:
        print(f"📭 {year}年{month}月 无记录")
        return

    income_total = sum(r["amount"] for r in filtered if r["type"] == "income")
    expense_total = sum(r["amount"] for r in filtered if r["type"] == "expense")

    print(f"\n{'='*45}")
    print(f"📊 {year}年{month}月 统计")
    print(f"{'='*45}")
    print(f"  📤 收入: ¥{income_total:>10.2f}")
    print(f"  💸 支出: ¥{expense_total:>10.2f}")
    print(f"  💰 结余: ¥{income_total - expense_total:>10.2f}")
    print(f"  📋 笔数: {len(filtered)}")

    # 分类统计
    cats = defaultdict(float)
    for r in filtered:
        cats[r["category"]] += r["amount"] if r["type"] == "expense" else 0

    if cats:
        print(f"\n  支出分类:")
        for cat, total in sorted(cats.items(), key=lambda x: -x[1]):
            pct = total / expense_total * 100 if expense_total else 0
            bar = "█" * int(pct // 5)
            print(f"    {cat:>4}  ¥{total:>8.2f}  {pct:>5.1f}%  {bar}")
    print(f"{'='*45}\n")


def cmd_help():
    """显示帮助"""
    print("""
💰 Expense Tracker - 记账工具

用法:
  python3 expense.py add -a <金额> -c <分类> [-n 备注] [-t income]
  python3 expense.py list [--days N] [--type income|expense]
  python3 expense.py summary [--month M] [--year Y]
  python3 expense.py categories

示例:
  python3 expense.py add -a 25 -c 餐饮 -n "午饭"
  python3 expense.py add -a 5000 -c 工资 -t income
  python3 expense.py list --days 7
  python3 expense.py summary --month 5

分类:
  支出: 餐饮、交通、购物、娱乐、住房、医疗、教育、其他
  收入: 工资、兼职、红包、投资、其他
""")


def cmd_categories():
    """显示分类列表"""
    print("\n📂 支出分类:", ", ".join(CATEGORIES_EXPENSE))
    print("📂 收入分类:", ", ".join(CATEGORIES_INCOME))
    print("\n💡 也可以用其他分类名，自由添加\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        cmd_help()
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "add":
        amount = None
        category = None
        note = ""
        ttype = "expense"

        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "-a" and i + 1 < len(sys.argv):
                amount = float(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == "-c" and i + 1 < len(sys.argv):
                category = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "-n" and i + 1 < len(sys.argv):
                note = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "-t" and i + 1 < len(sys.argv):
                ttype = sys.argv[i + 1]
                i += 2
            else:
                i += 1

        if amount is None or category is None:
            print("❌ 请提供金额(-a)和分类(-c)")
            sys.exit(1)

        add_record(amount, category, note, ttype)

    elif cmd == "list":
        days = None
        ttype = None
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--days" and i + 1 < len(sys.argv):
                days = int(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == "--type" and i + 1 < len(sys.argv):
                ttype = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        list_records(days, ttype)

    elif cmd == "summary":
        month = None
        year = None
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--month" and i + 1 < len(sys.argv):
                month = int(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == "--year" and i + 1 < len(sys.argv):
                year = int(sys.argv[i + 1])
                i += 2
            else:
                i += 1
        summary(month, year)

    elif cmd == "categories":
        cmd_categories()

    elif cmd in ("-h", "--help", "help"):
        cmd_help()

    else:
        print(f"❌ 未知命令: {cmd}")
        cmd_help()
