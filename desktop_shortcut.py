#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
桌面快捷方式启动器
"""

import sys
import os
from pathlib import Path

# 添加src目录到路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir / "src"))

def main():
    print("=== 番茄时钟启动 === ")
    print(f"项目目录: {current_dir}")

    try:
        from run_simple import main as run_app
        print("✓ 正在启动番茄时钟...")
        run_app()
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        print("尝试其他启动方式...")

        try:
            from start_pomodoro import main as run_app2
            run_app2()
        except Exception as e2:
            print(f"✗ 启动失败: {e2}")
            print("\n请确保已安装所需依赖:")
            print("  pip install PyQt6")
            input("按Enter键退出...")


if __name__ == "__main__":
    main()