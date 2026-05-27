#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
用户界面模块 - 现代简约风格
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QGridLayout, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon
import sys


class MainWindow(QMainWindow):
    """主窗口"""

    # 信号定义
    start_requested = pyqtSignal()
    pause_requested = pyqtSignal()
    reset_requested = pyqtSignal()
    skip_requested = pyqtSignal()
    mode_switch_requested = pyqtSignal(str)  # work, short_break, long_break

    def __init__(self):
        super().__init__()

        # 窗口设置
        self.setWindowTitle("番茄时钟 - Pomodoro Clock")
        self.setFixedSize(500, 600)  # 固定大小
        self.setStyleSheet(self._get_stylesheet())  # 设置样式

        # 创建中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 主布局
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # 初始化UI
        self._init_ui()

    def _get_stylesheet(self):
        """获取样式表"""
        return """
        QMainWindow {
            background-color: #f8f9fa;
        }

        QWidget {
            font-family: Arial, sans-serif;
        }

        QLabel {
            color: #333333;
        }

        QLabel#title_label {
            color: #2c3e50;
            font-weight: bold;
            font-size: 24px;
        }

        QLabel#time_label {
            color: #2c3e50;
            font-size: 64px;
            font-weight: bold;
        }

        QLabel#mode_label {
            color: #7f8c8d;
            font-size: 16px;
        }

        QLabel#count_label {
            color: #34495e;
            font-size: 14px;
        }

        QPushButton {
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: bold;
            font-size: 14px;
        }

        QPushButton#start_button {
            background-color: #2ecc71;
            color: white;
        }

        QPushButton#start_button:hover {
            background-color: #27ae60;
        }

        QPushButton#pause_button {
            background-color: #3498db;
            color: white;
        }

        QPushButton#pause_button:hover {
            background-color: #2980b9;
        }

        QPushButton#reset_button {
            background-color: #e74c3c;
            color: white;
        }

        QPushButton#reset_button:hover {
            background-color: #c0392b;
        }

        QPushButton#skip_button {
            background-color: #f39c12;
            color: white;
        }

        QPushButton#skip_button:hover {
            background-color: #d68910;
        }

        QPushButton#work_button {
            background-color: #3498db;
            color: white;
        }

        QPushButton#short_break_button {
            background-color: #9b59b6;
            color: white;
        }

        QPushButton#long_break_button {
            background-color: #1abc9c;
            color: white;
        }

        QPushButton.mode_button_active {
            border: 3px solid #2c3e50;
            padding: 9px 21px;
        }

        QFrame#time_frame {
            background-color: white;
            border-radius: 20px;
            border: 2px solid #e0e0e0;
        }

        QGroupBox {
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            margin-top: 10px;
            font-weight: bold;
            color: #34495e;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        """

    def _init_ui(self):
        """初始化UI组件"""

        # 1. 标题区域
        title_label = QLabel("🍅 番茄时钟")
        title_label.setObjectName("title_label")
        title_font = QFont("Arial", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)

        # 2. 时间显示区域
        time_frame = QFrame()
        time_frame.setObjectName("time_frame")
        time_frame.setFixedHeight(200)
        time_layout = QVBoxLayout(time_frame)
        time_layout.setContentsMargins(40, 40, 40, 40)

        # 时间显示标签
        self.time_label = QLabel("25:00")
        self.time_label.setObjectName("time_label")
        time_font = QFont("Arial", 64, QFont.Weight.Bold)
        self.time_label.setFont(time_font)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_layout.addWidget(self.time_label)

        # 模式显示标签
        self.mode_label = QLabel("工作模式")
        self.mode_label.setObjectName("mode_label")
        mode_font = QFont("Arial", 16)
        self.mode_label.setFont(mode_font)
        self.mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_layout.addWidget(self.mode_label)

        self.main_layout.addWidget(time_frame)

        # 3. 控制按钮区域
        control_group = QGroupBox("控制")
        control_layout = QGridLayout(control_group)
        control_layout.setSpacing(15)

        # 开始按钮
        self.start_button = QPushButton("▶ 开始")
        self.start_button.setObjectName("start_button")
        self.start_button.setFixedHeight(50)
        self.start_button.clicked.connect(self._on_start_clicked)
        control_layout.addWidget(self.start_button, 0, 0)

        # 暂停按钮
        self.pause_button = QPushButton("⏸ 暂停")
        self.pause_button.setObjectName("pause_button")
        self.pause_button.setFixedHeight(50)
        self.pause_button.clicked.connect(self._on_pause_clicked)
        control_layout.addWidget(self.pause_button, 0, 1)

        # 重置按钮
        self.reset_button = QPushButton("↻ 重置")
        self.reset_button.setObjectName("reset_button")
        self.reset_button.setFixedHeight(50)
        self.reset_button.clicked.connect(self._on_reset_clicked)
        control_layout.addWidget(self.reset_button, 1, 0)

        # 跳过按钮
        self.skip_button = QPushButton("⏭ 跳过")
        self.skip_button.setObjectName("skip_button")
        self.skip_button.setFixedHeight(50)
        self.skip_button.clicked.connect(self._on_skip_clicked)
        control_layout.addWidget(self.skip_button, 1, 1)

        self.main_layout.addWidget(control_group)

        # 4. 模式切换区域
        mode_group = QGroupBox("模式")
        mode_layout = QHBoxLayout(mode_group)
        mode_layout.setSpacing(15)

        # 工作模式按钮
        self.work_button = QPushButton("工作（25分钟）")
        self.work_button.setObjectName("work_button")
        self.work_button.setProperty("mode", "work")
        self.work_button.clicked.connect(lambda: self._on_mode_clicked("work"))
        mode_layout.addWidget(self.work_button)

        # 短休息按钮
        self.short_break_button = QPushButton("短休息（5分钟）")
        self.short_break_button.setObjectName("short_break_button")
        self.short_break_button.setProperty("mode", "short_break")
        self.short_break_button.clicked.connect(lambda: self._on_mode_clicked("short_break"))
        mode_layout.addWidget(self.short_break_button)

        # 长休息按钮
        self.long_break_button = QPushButton("长休息（15分钟）")
        self.long_break_button.setObjectName("long_break_button")
        self.long_break_button.setProperty("mode", "long_break")
        self.long_break_button.clicked.connect(lambda: self._on_mode_clicked("long_break"))
        mode_layout.addWidget(self.long_break_button)

        self.main_layout.addWidget(mode_group)

        # 5. 统计信息区域
        stats_group = QGroupBox("统计")
        stats_layout = QVBoxLayout(stats_group)

        self.count_label = QLabel("今日完成：0 个番茄钟")
        self.count_label.setObjectName("count_label")
        count_font = QFont("Arial", 14)
        self.count_label.setFont(count_font)
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_layout.addWidget(self.count_label)

        self.main_layout.addWidget(stats_group)

        # 6. 底部信息
        info_label = QLabel("按空格键开始/暂停 • 按 R 键重置 • 按 S 键跳过")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_font = QFont("Arial", 10)
        info_label.setFont(info_font)
        info_label.setStyleSheet("color: #7f8c8d;")
        self.main_layout.addWidget(info_label)

        # 添加弹性空间
        self.main_layout.addStretch(1)

        # 设置初始状态
        self._update_mode_buttons("work")

    def _on_start_clicked(self):
        """开始按钮点击事件"""
        self.start_requested.emit()

    def _on_pause_clicked(self):
        """暂停按钮点击事件"""
        self.pause_requested.emit()

    def _on_reset_clicked(self):
        """重置按钮点击事件"""
        self.reset_requested.emit()

    def _on_skip_clicked(self):
        """跳过按钮点击事件"""
        self.skip_requested.emit()

    def _on_mode_clicked(self, mode):
        """模式按钮点击事件"""
        self.mode_switch_requested.emit(mode)
        self._update_mode_buttons(mode)

    def _update_mode_buttons(self, active_mode):
        """更新模式按钮状态"""
        buttons = {
            "work": self.work_button,
            "short_break": self.short_break_button,
            "long_break": self.long_break_button
        }

        for mode, button in buttons.items():
            if mode == active_mode:
                button.setStyleSheet(button.styleSheet() + "border: 3px solid #2c3e50;")
            else:
                button.setStyleSheet(button.styleSheet().replace("border: 3px solid #2c3e50;", ""))

    @pyqtSlot(str)
    def update_time_display(self, time_str):
        """更新时间显示"""
        self.time_label.setText(time_str)

    @pyqtSlot(str)
    def update_mode_display(self, mode):
        """更新模式显示"""
        mode_names = {
            "work": "工作模式",
            "short_break": "短休息",
            "long_break": "长休息"
        }
        self.mode_label.setText(mode_names.get(mode, "未知模式"))

    @pyqtSlot(str)
    def update_state_display(self, state):
        """更新状态显示并调整按钮"""
        if state == "running":
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)
        elif state == "paused":
            self.start_button.setEnabled(True)
            self.start_button.setText("▶ 继续")
            self.pause_button.setEnabled(False)
        elif state == "stopped":
            self.start_button.setEnabled(True)
            self.start_button.setText("▶ 开始")
            self.pause_button.setEnabled(True)

    @pyqtSlot(int)
    def update_pomodoro_count(self, count):
        """更新番茄钟计数"""
        self.count_label.setText(f"今日完成：{count} 个番茄钟")

    @pyqtSlot(str)
    def show_notification(self, message):
        """显示通知（在状态栏显示）"""
        self.statusBar().showMessage(message, 3000)  # 显示3秒

    def keyPressEvent(self, event):
        """键盘事件处理"""
        if event.key() == Qt.Key.Key_Space:
            self._on_start_clicked()
        elif event.key() == Qt.Key.Key_R:
            self._on_reset_clicked()
        elif event.key() == Qt.Key.Key_S:
            self._on_skip_clicked()
        elif event.key() == Qt.Key.Key_Escape:
            self.showMinimized()
        elif event.key() == Qt.Key.Key_Q and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.close()
        else:
            super().keyPressEvent(event)