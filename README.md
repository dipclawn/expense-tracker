# 💰 Expense Tracker - 极简记账工具

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

一个纯 Python 的命令行记账工具，零依赖，数据存本地 JSON 文件。  
同时提供 **Web 版** 和 **APK 打包脚本**，PC / 手机 / 安卓都能用。

---

## ✨ 功能

| 功能 | 命令 |
|------|------|
| 💸 记支出 | `python3 expense.py add -a 25 -c 餐饮 -n "午饭"` |
| 📤 记收入 | `python3 expense.py add -a 5000 -c 工资 -t income` |
| 📋 查看账单 | `python3 expense.py list --days 7` |
| 📊 月统计+预算对比 | `python3 expense.py summary --month 5` |
| 🎯 设置预算 | `python3 expense.py budget -c 餐饮 -a 2000` |
| 🗑️ 删除/编辑 | `python3 expense.py del 1` / `edit 1 -n "新备注"` |
| 📤 导出CSV | `python3 expense.py export` |

---

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

---

## 📱 多平台使用

### 🌐 Web 版（推荐，手机即用）

浏览器打开 `index.html` 即可使用，数据存在浏览器本地。  
也可以部署到 GitHub Pages：
```
Settings → Pages → Deploy from branch → main → / (root)
```

### 🐍 Python 直接运行

任何有 Python 的设备：
```bash
python3 expense.py
```

### 📦 打包成 APK（Android）

```bash
# 需要 Linux 环境
pip install buildozer cython
buildozer android debug
```

### 💻 打包成 EXE（Windows）

```bash
pip install pyinstaller
pyinstaller --onefile expense.py
```

---

## 📂 数据

存储在 `~/.expense-tracker/data.json`，纯 JSON 格式，可手动编辑或备份。

**Web 版：** 数据存在浏览器 localStorage 中，与命令行版不互通。

---

## 🔧 技术栈

- Python 3 标准库（零第三方依赖）
- 纯前端 HTML + CSS + JS（Web 版）
- Buildozer（APK 打包）
- MIT License

---

## 📜 License

MIT - 随便用，随便改，欢迎 PR！
