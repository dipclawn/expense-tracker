# 💰 Expense Tracker - 极简记账工具

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

一个纯 Python 的命令行记账工具，零依赖，数据存本地 JSON 文件。

## ✨ 功能

| 功能 | 命令 |
|------|------|
| 💸 记支出 | `add -a 25 -c 餐饮 -n "午饭"` |
| 📤 记收入 | `add -a 5000 -c 工资 -t income` |
| 📋 查看账单 | `list --days 7` |
| 📊 月统计+预算对比 | `summary --month 5` |
| 🎯 设置预算 | `budget -c 餐饮 -a 2000` |
| 🗑️ 删除/编辑 | `del 1` / `edit 1 -n "新备注"` |
| 📤 导出CSV | `export` |

## 🚀 快速开始

```bash
# 下载
git clone https://github.com/dipclawn/expense-tracker.git
cd expense-tracker

# 记一笔
python3 expense.py add -a 25 -c 餐饮 -n "午饭"

# 查看本月账单
python3 expense.py list

# 查看统计
python3 expense.py summary
```

## 🏗️ 打包安装 (Android / PC)

### 方式一：Python 直接运行（推荐）

```bash
python3 expense.py
```

### 方式二：打包成 APK（Android）

```bash
# 需要 Python-for-Android / Buildozer 环境
pip install buildozer cython
buildozer android debug
```

### 方式三：打包成 EXE（Windows）

```bash
pip install pyinstaller
pyinstaller --onefile expense.py
```

## 📱 Web 版

浏览器也能用 → 在项目目录运行：
```bash
python3 -m http.server 8080
```
然后访问 http://localhost:8080/web/

## 📂 数据

存储在 `~/.expense-tracker/data.json`，纯 JSON 格式，可手动编辑或备份。

## 📜 License

MIT
