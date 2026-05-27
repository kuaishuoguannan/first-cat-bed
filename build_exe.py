#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
打包番茄时钟为可执行文件
"""

import PyInstaller.__main__
import os
import sys
from pathlib import Path

def build_exe():
    """打包应用为EXE"""

    print("正在打包番茄时钟为可执行文件...")
    print(f"当前目录: {os.getcwd()}")

    # 创建资源文件夹
    resources = Path("resources")
    icons_dir = resources / "icons"
    sounds_dir = resources / "sounds"

    icons_dir.mkdir(parents=True, exist_ok=True)
    sounds_dir.mkdir(parents=True, exist_ok=True)

    # PyInstaller参数
    pyinstaller_args = [
        "run_simple.py",                    # 主脚本
        "--onefile",                        # 打包为单个EXE文件
        "--windowed",                       # 窗口应用（不显示控制台）
        f"--name=PomodoroClock",            # 输出的EXE名称
        f"--icon={(icons_dir / 'pomodoro.ico').as_posix()}",  # 图标
        f"--add-data={(resources).as_posix()}{os.pathsep}resources",  # 资源文件
        "--clean",                          # 清理临时文件
        "--noconfirm",                      # 不确认输出目录
    ]

    try:
        PyInstaller.__main__.run(pyinstaller_args)
        print("\n✅ 打包成功!")
        print(f"EXE文件位置: dist/PomodoroClock.exe")
        print("\n可以将 dist/PomodoroClock.exe 复制到桌面")
    except Exception as e:
        print(f"\n❌ 打包失败: {e}")
        print("\n可以尝试手动打包:")
        print("1. 安装打包工具: pip install pyinstaller")
        print("2. 运行: pyinstaller --onefile --windowed run_simple.py")

        # 尝试手动说明
        print("\n手动打包步骤:")
        print("-" * 40)
        print("1. 打开命令提示符")
        print("2. cd E:\\Cursor\\first CC")
        print("3. pip install pyinstaller")
        print("4. pyinstaller --onefile --windowed run_simple.py")
        print("-" * 40)

if __name__ == "__main__":
    build_exe()