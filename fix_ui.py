#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
修复UI样式，移除不支持的CSS属性
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class SimplePomodoroWindow(QMainWindow):
    """简单番茄时钟窗口"""

    def __init__(self):
        super().__init__()

        # 窗口设置
        self.setWindowTitle("番茄时钟")
        self.setFixedSize(450, 500)

        # 中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 主布局
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }

            QLabel#time_label {
                color: #2c3e50;
                font-size: 72px;
                font-weight: bold;
            }

            QLabel#mode_label {
                color: #7f8c8d;
                font-size: 18px;
            }

            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 15px 0;
                font-size: 16px;
                font-weight: bold;
                margin: 5px;
            }

            QPushButton#start_btn {
                background-color: #2ecc71;
                color: white;
            }

            QPushButton#start_btn:hover {
                background-color: #27ae60;
            }

            QPushButton#pause_btn {
                background-color: #3498db;
                color: white;
            }

            QPushButton#pause_btn:hover {
                background-color: #2980b9;
            }

            QPushButton#reset_btn {
                background-color: #e74c3c;
                color: white;
            }

            QPushButton#reset_btn:hover {
                background-color: #c0392b;
            }

            QFrame#time_frame {
                background-color: white;
                border-radius: 15px;
                border: 2px solid #e0e0e0;
            }
        """)

        # 创建UI
        self._create_ui()

    def _create_ui(self):
        """创建UI组件"""

        # 时间显示框架
        time_frame = QFrame()
        time_frame.setObjectName("time_frame")
        time_frame.setFixedHeight(200)
        time_layout = QVBoxLayout(time_frame)

        # 时间显示
        self.time_label = QLabel("25:00")
        self.time_label.setObjectName("time_label")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_layout.addWidget(self.time_label)

        # 模式显示
        self.mode_label = QLabel("工作模式")
        self.mode_label.setObjectName("mode_label")
        self.mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_layout.addWidget(self.mode_label)

        self.main_layout.addWidget(time_frame)

        # 控制按钮
        control_layout = QHBoxLayout()

        # 开始按钮
        self.start_btn = QPushButton("开始")
        self.start_btn.setObjectName("start_btn")
        self.start_btn.clicked.connect(lambda: print("开始"))
        control_layout.addWidget(self.start_btn)

        # 暂停按钮
        self.pause_btn = QPushButton("暂停")
        self.pause_btn.setObjectName("pause_btn")
        self.pause_btn.clicked.connect(lambda: print("暂停"))
        control_layout.addWidget(self.pause_btn)

        # 重置按钮
        self.reset_btn = QPushButton("重置")
        self.reset_btn.setObjectName("reset_btn")
        self.reset_btn.clicked.connect(lambda: print("重置"))
        control_layout.addWidget(self.reset_btn)

        self.main_layout.addLayout(control_layout)

        # 模式按钮
        mode_layout = QHBoxLayout()

        work_btn = QPushButton("工作 (25m)")
        work_btn.setStyleSheet("background-color: #3498db; color: white;")
        work_btn.clicked.connect(lambda: self.set_mode("工作"))
        mode_layout.addWidget(work_btn)

        short_break_btn = QPushButton("短休息 (5m)")
        short_break_btn.setStyleSheet("background-color: #9b59b6; color: white;")
        short_break_btn.clicked.connect(lambda: self.set_mode("短休息"))
        mode_layout.addWidget(short_break_btn)

        long_break_btn = QPushButton("长休息 (15m)")
        long_break_btn.setStyleSheet("background-color: #1abc9c; color: white;")
        long_break_btn.clicked.connect(lambda: self.set_mode("长休息"))
        mode_layout.addWidget(long_break_btn)

        self.main_layout.addLayout(mode_layout)

        # 统计信息
        stats_label = QLabel("今日完成: 0 个番茄钟")
        stats_label.setStyleSheet("color: #34495e; font-size: 14px;")
        stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(stats_label)

        # 提示信息
        hint_label = QLabel("快捷操作: 空格键开始/暂停 • R键重置 • S键跳过")
        hint_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(hint_label)

        # 添加弹性空间
        self.main_layout.addStretch(1)

    def set_mode(self, mode):
        """设置模式"""
        if mode == "工作":
            self.time_label.setText("25:00")
        elif mode == "短休息":
            self.time_label.setText("05:00")
        elif mode == "长休息":
            self.time_label.setText("15:00")
        self.mode_label.setText(mode)


def main():
    """主函数"""
    app = QApplication(sys.argv)
    window = SimplePomodoroWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()