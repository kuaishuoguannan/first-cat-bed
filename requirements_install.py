#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
安装依赖脚本
如果 pip install -r requirements.txt 失败，可以运行此脚本
"""

import subprocess
import sys
import os


def install_requirements():
    """安装所有依赖包"""
    requirements = [
        "PyQt6>=6.6.0",
        "pyqt6-tools>=6.6.0",
        "pygame>=2.5.0",
        "plyer>=2.1.0",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "python-dateutil>=2.8.2",
        "psutil>=5.9.0",
        "colorthief>=0.2.1",  # 可选
    ]

    print("开始安装番茄时钟依赖包...")
    print(f"Python版本: {sys.version}")
    print(f"工作目录: {os.getcwd()}")
    print("-" * 50)

    successful = []
    failed = []

    for req in requirements:
        print(f"正在安装: {req}")
        try:
            # 使用国内镜像源加速下载
            result = subprocess.run(
                [
                    sys.executable, "-m", "pip", "install",
                    req, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"
                ],
                capture_output=True,
                text=True,
                check=True
            )
            # 检查是否安装成功
            if "Successfully installed" in result.stdout or "Requirement already satisfied" in result.stdout:
                successful.append(req)
                print(f"✓ {req} 安装成功")
            else:
                failed.append(req)
                print(f"✗ {req} 安装失败")
                if result.stderr:
                    print(f"  错误信息: {result.stderr[:200]}...")

        except subprocess.CalledProcessError as e:
            failed.append(req)
            print(f"✗ {req} 安装失败")
            if e.stderr:
                print(f"  错误信息: {e.stderr[:200]}...")

        print("-" * 30)

    print("\n安装结果:")
    print(f"成功: {len(successful)} 个")
    print(f"失败: {len(failed)} 个")

    if failed:
        print("\n尝试使用基础依赖安装...")
        # 只安装基本必要的包
        basic_requirements = ["PyQt6>=6.6.0", "pyqt6-tools>=6.6.0"]
        basic_success = []
        basic_failed = []

        for req in basic_requirements:
            if req in failed or req not in successful:
                print(f"正在安装基本依赖: {req}")
                try:
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", req],
                        capture_output=True,
                        text=True
                    )
                    if "Successfully installed" in result.stdout or "Requirement already satisfied" in result.stdout:
                        basic_success.append(req)
                        print(f"✓ {req} 安装成功")
                    else:
                        basic_failed.append(req)
                        print(f"✗ {req} 安装失败")
                except Exception:
                    basic_failed.append(req)

        if basic_failed:
            print(f"\n基本依赖安装失败: {basic_failed}")
            print("请手动安装PyQt6:")
            print("  pip install PyQt6 pyqt6-tools")
            return False

    print(f"\n所有依赖包安装完成!")
    return True


def check_requirements():
    """检查是否已安装所有依赖"""
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
        if module == "dateutil":
            module = "dateutil"  # python-dateutil模块名是dateutil
        spec = importlib.util.find_spec(module)
        if spec is None:
            missing.append(module)

    if missing:
        print(f"缺少以下模块: {missing}")
        return False
    else:
        print("所有依赖模块已安装")
        return True


if __name__ == "__main__":
    print("=" * 50)
    print("番茄时钟依赖安装脚本")
    print("=" * 50)

    if check_requirements():
        print("依赖检查通过，无需安装")
        sys.exit(0)

    user_input = input("检测到缺少依赖，是否安装? (y/n): ").strip().lower()
    if user_input in ["y", "yes", "是"]:
        if install_requirements():
            print("\n安装完成! 可以运行番茄时钟了")
            print("运行命令: python src/main.py 或 python run.py")
        else:
            print("\n安装失败，请手动安装依赖")
            sys.exit(1)
    else:
        print("安装已取消")
        sys.exit(0)
        