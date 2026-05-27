#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
运行简单但好看的番茄时钟
"""

import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QFrame)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


class SimplePomodoroTimer:
    """简单番茄时钟计时器"""
    def __init__(self):
        self.work_time = 25 * 60  # 25分钟
        self.short_break = 5 * 60  # 5分钟
        self.long_break = 15 * 60  # 15分钟
        self.time_left = self.work_time
        self.is_running = False
        self.mode = "work"  # work, short_break, long_break
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)

    def update_time(self):
        """更新时间"""
        if self.time_left > 0:
            self.time_left -= 1
        else:
            self.timer.stop()
            self.is_running = False
            print("时间到！")

    def start(self):
        """开始"""
        if not self.is_running:
            self.is_running = True
            self.timer.start(1000)  # 1秒间隔

    def pause(self):
        """暂停"""
        if self.is_running:
            self.is_running = False
            self.timer.stop()

    def reset(self):
        """重置"""
        self.pause()
        if self.mode == "work":
            self.time_left = self.work_time
        elif self.mode == "short_break":
            self.time_left = self.short_break
        elif self.mode == "long_break":
            self.time_left = self.long_break

    def set_mode(self, mode):
        """设置模式"""
        self.mode = mode
        self.reset()


class PomodoroWindow(QMainWindow):
    """番茄时钟窗口"""

    def __init__(self):
        super().__init__()
        self.timer = SimplePomodoroTimer()
        self.init_ui()
        self.update_display()

    def init_ui(self):
        """初始化UI"""
        # 窗口设置
        self.setWindowTitle("番茄时钟")
        self.setFixedSize(500, 550)

        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # 标题
        title = QLabel("🍅 番茄时钟")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)

        # 时间显示框架
        time_frame = QFrame()
        time_frame.setFixedSize(300, 200)
        time_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 25px;
                border: 3px solid #e0e0e0;
            }
        """)

        time_layout = QVBoxLayout(time_frame)
        time_layout.setContentsMargins(20, 20, 20, 20)

        # 时间显示
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Arial", 72, QFont.Weight.Bold))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("color: #2c3e50;")
        time_layout.addWidget(self.time_label)

        # 模式显示
        self.mode_label = QLabel()
        self.mode_label.setFont(QFont("Arial", 18))
        self.mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mode_label.setStyleSheet("color: #7f8c8d; margin-top: 10px;")
        time_layout.addWidget(self.mode_label)

        layout.addWidget(time_frame, 0, Qt.AlignmentFlag.AlignCenter)

        # 控制按钮
        control_layout = QHBoxLayout()
        control_layout.setSpacing(15)

        self.start_btn = self.create_button("开始", "#2ecc71")
        self.start_btn.clicked.connect(self.start_timer)
        control_layout.addWidget(self.start_btn)

        self.pause_btn = self.create_button("暂停", "#3498db")
        self.pause_btn.clicked.connect(self.pause_timer)
        control_layout.addWidget(self.pause_btn)

        self.reset_btn = self.create_button("重置", "#e74c3c")
        self.reset_btn.clicked.connect(self.reset_timer)
        control_layout.addWidget(self.reset_btn)

        layout.addLayout(control_layout)

        # 模式按钮
        mode_layout = QHBoxLayout()
        mode_layout.setSpacing(15)

        work_btn = self.create_button("工作 (25分钟)", "#3498db")
        work_btn.clicked.connect(lambda: self.set_mode("work"))
        mode_layout.addWidget(work_btn)

        short_break_btn = self.create_button("短休息 (5分钟)", "#9b59b6")
        short_break_btn.clicked.connect(lambda: self.set_mode("short_break"))
        mode_layout.addWidget(short_break_btn)

        long_break_btn = self.create_button("长休息 (15分钟)", "#1abc9c")
        long_break_btn.clicked.connect(lambda: self.set_mode("long_break"))
        mode_layout.addWidget(long_break_btn)

        layout.addLayout(mode_layout)

        # 统计信息
        stats_label = QLabel("今日完成: 0 个番茄钟")
        stats_label.setFont(QFont("Arial", 14))
        stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_label.setStyleSheet("color: #34495e; margin-top: 20px;")
        layout.addWidget(stats_label)

        # 提示信息
        hint_label = QLabel("快捷操作: 空格键开始/暂停 • R键重置 • S键跳过 • Esc最小化")
        hint_label.setFont(QFont("Arial", 11))
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint_label.setStyleSheet("color: #7f8c8d; margin-top: 20px;")
        layout.addWidget(hint_label)

        # 添加弹性空间
        layout.addStretch()

        # 连接计时器更新
        self.timer.timer.timeout.connect(self.update_display)

    def create_button(self, text, color):
        """创建按钮"""
        btn = QPushButton(text)
        btn.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        btn.setFixedHeight(50)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
        """)
        return btn

    def darken_color(self, color):
        """加深颜色"""
        # 简单的颜色加深（移除#号，转换为RGB）
        color = color.lstrip('#')
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)

        # 减少亮度
        r = max(0, r - 30)
        g = max(0, g - 30)
        b = max(0, b - 30)

        return f"#{r:02x}{g:02x}{b:02x}"

    def format_time(self, seconds):
        """格式化时间"""
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def update_display(self):
        """更新显示"""
        self.time_label.setText(self.format_time(self.timer.time_left))

        # 更新模式标签
        if self.timer.mode == "work":
            self.mode_label.setText("工作模式")
        elif self.timer.mode == "short_break":
            self.mode_label.setText("短休息")
        elif self.timer.mode == "long_break":
            self.mode_label.setText("长休息")

    def start_timer(self):
        """开始计时器"""
        self.timer.start()
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)

    def pause_timer(self):
        """暂停计时器"""
        self.timer.pause()
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)

    def reset_timer(self):
        """重置计时器"""
        self.timer.reset()
        self.update_display()
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(True)

    def set_mode(self, mode):
        """设置模式"""
        self.timer.set_mode(mode)
        self.update_display()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 使用Fusion样式，在所有平台看起来一致

    # 设置应用信息
    app.setApplicationName("番茄时钟")
    app.setApplicationDisplayName("番茄时钟")

    # 创建窗口
    window = PomodoroWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()