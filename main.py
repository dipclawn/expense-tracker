#!/usr/bin/env python3
"""
Expense Tracker - 入口文件
Python直接运行，也可供Buildozer打包
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from expense import *

if __name__ == "__main__":
    print("""
💰 Expense Tracker v2.0
=======================
数据存储在 ~/.expense-tracker/data.json

快速开始:
  python3 main.py add -a 25 -c 餐饮 -n "午饭"
  python3 main.py list
  python3 main.py summary
  python3 main.py help
""")
    if len(sys.argv) > 1:
        cmd, args = parse_args()
        if cmd in COMMANDS:
            COMMANDS[cmd](args)
        else:
            print(f"❌ 未知命令: {cmd}")
            cmd_help()
