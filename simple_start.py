#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简化启动脚本
跳过依赖检查，直接运行番茄时钟
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("=" * 50)
    print("番茄时钟 - 简化启动")
    print("=" * 50)

    try:
        # 检查基本依赖
        import importlib.util

        # 必需模块
        required_modules = ["PyQt6"]

        missing = []
        for module in required_modules:
            spec = importlib.util.find_spec(module)
            if spec is None:
                missing.append(module)

        if missing:
            print(f"错误: 缺少必需模块: {missing}")
            print("请安装: pip install PyQt6")
            return 1

        print("[OK] PyQt6 已安装")

        # 尝试导入
        print("正在导入模块...")
        from ui import MainWindow
        from timer import PomodoroTimer
        from PyQt6.QtWidgets import QApplication

        print("[OK] 模块导入成功")

        # 创建应用
        app = QApplication(sys.argv)
        app.setApplicationName("Pomodoro Clock")
        app.setApplicationDisplayName("番茄时钟")

        window = MainWindow()
        timer = PomodoroTimer()

        # 简单连接信号
        window.start_requested.connect(timer.start)
        window.pause_requested.connect(timer.pause)
        window.reset_requested.connect(timer.reset)
        window.skip_requested.connect(timer.skip)

        timer.time_changed.connect(window.update_time_display)
        timer.mode_changed.connect(window.update_mode_display)
        timer.state_changed.connect(window.update_state_display)

        # 设置初始显示
        window.update_time_display("25:00")
        window.update_mode_display("work")
        window.update_state_display("stopped")

        print("[OK] 应用初始化完成")
        print("=" * 50)
        print("启动番茄时钟...")
        print("按空格键开始/暂停 • 按R键重置 • 按S键跳过")

        window.show()
        sys.exit(app.exec())

    except ImportError as e:
        print(f"导入错误: {e}")
        print("\n请确保已安装所有依赖:")
        print("1. pip install PyQt6")
        print("2. pip install pygame plyer psutil (可选)")
        return 1
    except Exception as e:
        print(f"启动失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())