<div align="center">

# 💰 Expense Tracker

**极简记账工具** · Python · PWA · 手机即用

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue)](https://python.org)
[![PWA](https://img.shields.io/badge/PWA-✅-brightgreen)](https://dipclawn.github.io/expense-tracker/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

[🌐 在线使用](https://dipclawn.github.io/expense-tracker/) · 
[📦 GitHub](https://github.com/dipclawn/expense-tracker) · 
[📖 文档](#)

</div>

---

## ✨ 功能一览

| 功能 | 命令行 | Web版 |
|------|--------|-------|
| 💸 记支出 | `add -a 25 -c 餐饮` | ✅ 点一点就记 |
| 📤 记收入 | `add -a 5000 -c 工资 -t income` | ✅ |
| 📋 账单列表 | `list --days 7` | ✅ 按天筛选 |
| 📊 月度统计 | `summary --month 5` | ✅ 图表可视化 |
| 🎯 预算管理 | `budget -c 餐饮 -a 2000` | ✅ 进度对比 |
| 🔍 分类汇总 | `categories` | ✅ 柱状图分布 |
| 📤 导出数据 | `export` | ✅ JSON导出/导入 |
| 🗑️ 编辑删除 | `del 1` / `edit 1 -n "新备注"` | ✅ 点击删除 |

---

## 🚀 快速开始

### 🌐 Web版（推荐，手机即用）

**无需安装，打开浏览器就能记账：**

👉 https://dipclawn.github.io/expense-tracker/

- 可安装到手机桌面（Android: 菜单→添加到主屏幕）
- 离线可用（PWA Service Worker）
- 数据存在浏览器本地，不传服务器

### 🐍 命令行版

```bash
# 下载
git clone https://github.com/dipclawn/expense-tracker.git
cd expense-tracker

# 记一笔支出
python3 expense.py add -a 25 -c 餐饮 -n "午饭"

# 记一笔收入
python3 expense.py add -a 5000 -c 工资 -t income -n "5月工资"

# 查看今天账单
python3 expense.py list

# 查看本月统计（含预算对比）
python3 expense.py summary

# 设置预算
python3 expense.py budget -c 餐饮 -a 2000
python3 expense.py budget -c 娱乐 -a 800

# 删除/修改
python3 expense.py del 1
python3 expense.py edit 1 -n "新备注"

# 导出CSV
python3 expense.py export
```

### 📱 打包成APK

```bash
# 需要 Linux + Android SDK
pip install buildozer cython
python3 build_apk.py
buildozer android debug
```

---

## 📊 统计功能

### 月度财务报告
```
📊 2026年5月 财务报告
  📤 收入: ¥   5000.00
  💸 支出: ¥    343.00
  💰 结余: ¥   4657.00

  📊 支出分布:
    娱乐  ¥300.00  87.5%  █████████████████████
    餐饮  ¥ 25.00   7.3%  █
    交通  ¥ 18.00   5.2%  █

  🎯 预算对比:
    餐饮  ¥25/2000  ░░░░░░░░  1% ✅
    娱乐  ¥300/800  ▓▓▓▓▓▓░░ 38% ✅
```

### 每日支出趋势

Web版自动生成每日支出柱状图，一眼看清哪天花多了。

---

## 📁 数据存储

| 版本 | 存储位置 | 格式 |
|------|----------|------|
| 命令行 | `~/.expense-tracker/data.json` | JSON |
| Web版 | 浏览器 localStorage | JSON |

数据完全由你掌控，可导出备份、可手动编辑。

---

## 🛠️ 技术栈

- **Python 3** — 零第三方依赖，纯标准库
- **HTML + CSS + JS** — 纯前端PWA应用
- **Buildozer** — Android APK打包
- **GitHub Pages** — 免费托管Web版

## 📜 License

MIT — 随便用，随便改，欢迎 PR！

---

<div align="center">
  <sub>Made with ❤️ by <a href="https://github.com/dipclawn">dipclawn</a></sub>
</div>
