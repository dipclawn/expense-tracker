#!/usr/bin/env python3
"""
Expense Tracker APK 打包工具
用 Buildozer 将 Python 脚本打包成 Android APK
"""

import os
import sys
import subprocess
import shutil

def check_deps():
    """检查打包依赖"""
    deps = {"buildozer": "pip install buildozer",
            "cython": "pip install cython",
            "java": "apt install openjdk-17-jdk",
            "sdkmanager": "需要 Android SDK"}
    
    print("🔍 检查打包环境...")
    missing = []
    for cmd, install in deps.items():
        if not shutil.which(cmd):
            missing.append(f"  ❌ {cmd} - {install}")
    
    if missing:
        print("缺少以下依赖:")
        for m in missing:
            print(m)
        return False
    
    print("✅ 环境就绪")
    return True


def create_spec():
    """创建 Buildozer 配置文件"""
    spec = """[app]
title = 记账本
package.name = expense
package.domain = com.expensetracker
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

# Android 特定配置
[app]
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 34
android.ndk = 25b
android.gradle_dependencies = 
"""
    with open("buildozer.spec", "w") as f:
        f.write(spec)
    print("✅ buildozer.spec 已创建")


def build_apk():
    """执行打包"""
    print("📦 正在打包 APK...")
    print("   这需要 5-10 分钟，请确保网络畅通")
    
    if not check_deps():
        print("\n💡 在本地开发机上运行:")
        print("   pip install buildozer cython")
        print("   buildozer android debug")
        return False
    
    result = subprocess.run(["buildozer", "android", "debug"], 
                          capture_output=True, text=True, timeout=600)
    if result.returncode == 0:
        print("✅ APK 打包成功!")
        print(f"   文件在 bin/ 目录下")
    else:
        print(f"❌ 打包失败: {result.stderr}")
    return result.returncode == 0


def android_main():
    """Kivy 版 Android 入口 - 供 buildozer 打包用"""
    print("📱 Expense Tracker Android 版本")
    print("   请在手机上运行")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "android":
        android_main()
    else:
        print("""
📱 Expense Tracker APK 打包工具

用法:
  python3 build_apk.py          查看说明
  python3 build_apk.py android  Kivy入口（打包用）

打包步骤:
  1. 安装依赖: pip install buildozer cython
  2. 创建配置: python3 build_apk.py（自动创建 buildozer.spec）
  3. 打包:      buildozer android debug
  
注意:
  buildozer 需要 Linux 环境 + Android SDK
  首次打包会自动下载 SDK/NDK（约 2GB）
  
💡 也可以直接用 Web 版:
  用浏览器打开 index.html 即可使用
  或部署到 GitHub Pages: settings → Pages → main → / (root)
""")
