#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
启动脚本
自动检查依赖并启动应用
"""

import os
import sys
import subprocess
from pathlib import Path


def check_requirements():
    """检查是否已安装所有依赖"""
    try:
        # 尝试导入主要依赖
        import importlib.util

        required_modules = [
            "PyQt6",
            "pygame",
            "plyer",
            "pandas",
            "matplotlib",
            "dateutil",
            "psutil",
        ]

        missing = []
        for module in required_modules:
            # python-dateutil 的模块名是 dateutil
            if module == "dateutil":
                module_name = "dateutil"
            else:
                module_name = module.lower()

            spec = importlib.util.find_spec(module_name)
            if spec is None:
                missing.append(module)

        if missing:
            print(f"缺少以下模块: {missing}")
            return False
        return True

    except Exception as e:
        print(f"检查依赖时出错: {e}")
        return False


def install_requirements():
    """安装缺失的依赖"""
    print("正在安装缺失的依赖...")

    # 基础依赖列表
    basic_requirements = [
        "PyQt6>=6.6.0",
        "pyqt6-tools>=6.6.0",
        "pygame>=2.5.0",
        "plyer>=2.1.0",
        "psutil>=5.9.0",
    ]

    try:
        for req in basic_requirements:
            print(f"安装 {req}...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", req, "-q"]
            )
        return True
    except subprocess.CalledProcessError as e:
        print(f"安装依赖失败: {e}")
        return False


def create_resources():
    """创建资源文件夹"""
    resources_dir = Path("resources")

    # 创建文件夹结构
    folders = ["sounds", "icons", "themes"]
    for folder in folders:
        folder_path = resources_dir / folder
        folder_path.mkdir(parents=True, exist_ok=True)

    # 创建默认的图标文件占位符
    icon_dir = resources_dir / "icons"
    icon_files = ["pomodoro.ico", "pomodoro.png", "tray_icon.ico"]

    for icon_file in icon_files:
        icon_path = icon_dir / icon_file
        if not icon_path.exists():
            # 创建空文件作为占位符
            icon_path.touch()
            print(f"创建占位符文件: {icon_path}")

def run_app():
    """运行应用"""
    try:
        # 导入并运行应用
        sys.path.insert(0, "src")
        from src.main import main

        print("启动番茄时钟...")
        return main()
    except Exception as e:
        print(f"启动应用失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main():
    """主函数"""
    print("=" * 50)
    print("番茄时钟启动器")
    print("=" * 50)

    # 检查是否在项目根目录
    current_dir = Path.cwd()
    src_dir = current_dir / "src"
    if not src_dir.exists():
        print("错误: 请在项目根目录运行此脚本")
        print(f"当前目录: {current_dir}")
        print("请确保存在 src 文件夹")
        return 1

    # 创建资源文件夹
    create_resources()

    # 检查依赖
    if not check_requirements():
        print("检测到缺失的依赖")
        user_input = input("是否自动安装? (y/n): ").strip().lower()
        if user_input in ["y", "yes", "是"]:
            if not install_requirements():
                print("依赖安装失败，请手动运行 requirements_install.py")
                print("或执行: pip install PyQt6 pygame plyer psutil")
                return 1
        else:
            print("请手动安装依赖:")
            print("  pip install PyQt6 pygame plyer psutil")
            return 1

    # 运行应用
    print("=" * 50)
    return run_app()


if __name__ == "__main__":
    sys.exit(main())