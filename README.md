# 💰 Expense Tracker - 极简记账工具

一个命令行记账工具，轻量、无依赖、数据存本地 JSON 文件。

## 功能

- ✅ 记一笔账（收入/支出）
- ✅ 查看账单列表
- ✅ 查看月/周统计
- ✅ 分类汇总
- ✅ 数据导出

## 快速开始

```bash
# 记一笔支出
python3 expense.py add -a 25 -c 餐饮 -n "午饭"

# 记一笔收入
python3 expense.py add -a 5000 -c 工资 -t income -n "5月工资"

# 查看今天账单
python3 expense.py list

# 查看本月统计
python3 expense.py summary --month 5

# 查看分类统计
python3 expense.py categories
```

## 分类

| 类型 | 默认分类 |
|------|----------|
| 支出 | 餐饮、交通、购物、娱乐、住房、医疗、教育、其他 |
| 收入 | 工资、兼职、红包、投资、其他 |

## 数据

数据保存在 `~/.expense-tracker/data.json`，纯 JSON 格式，安全可控。
