#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# 设置编码
sys.stdout.reconfigure(encoding='utf-8')

def main():
    try:
        # 检查PyQt6
        import importlib.util
        spec = importlib.util.find_spec('PyQt6')
        if spec is None:
            print("ERROR: PyQt6 not installed!")
            print("Please run: pip install PyQt6")
            return 1

        # 导入模块
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

        try:
            from ui import MainWindow
            from timer import PomodoroTimer
            from PyQt6.QtWidgets import QApplication
            from PyQt6.QtCore import QCoreApplication
        except ImportError as e:
            print(f"Import error: {e}")
            print("Make sure all required modules are installed")
            return 1

        # 创建应用
        app = QApplication(sys.argv)
        app.setApplicationName("Pomodoro Clock")

        window = MainWindow()
        timer = PomodoroTimer()

        # 连接信号
        window.start_requested.connect(timer.start)
        window.pause_requested.connect(timer.pause)
        window.reset_requested.connect(timer.reset)
        window.skip_requested.connect(timer.skip)

        def on_mode_request(mode):
            if mode == "work":
                timer.switch_to_work()
            elif mode == "short_break":
                timer.switch_to_short_break()
            elif mode == "long_break":
                timer.switch_to_long_break()

        window.mode_switch_requested.connect(on_mode_request)

        timer.time_changed.connect(window.update_time_display)
        timer.time_finished.connect(window.show_notification)
        timer.mode_changed.connect(window.update_mode_display)
        timer.state_changed.connect(window.update_state_display)

        # 设置初始显示
        window.update_time_display("25:00")
        window.update_mode_display("work")
        window.update_state_display("stopped")

        window.show()
        print("Pomodoro Clock started!")
        print("Controls: Space=Start/Pause, R=Reset, S=Skip, Esc=Minimize, Ctrl+Q=Quit")
        return app.exec()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())