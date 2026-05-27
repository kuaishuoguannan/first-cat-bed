#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
计时器核心逻辑模块
"""

from PyQt6.QtCore import QTimer, pyqtSignal, QObject
import time


class PomodoroTimer(QObject):
    """番茄钟计时器类"""

    # 信号定义
    time_changed = pyqtSignal(str)  # 时间变化信号
    time_finished = pyqtSignal(str)  # 计时结束信号
    mode_changed = pyqtSignal(str)  # 模式变化信号
    state_changed = pyqtSignal(str)  # 状态变化信号

    def __init__(self, parent=None):
        super().__init__(parent)

        # 默认配置
        self.work_minutes = 25  # 工作时间（分钟）
        self.short_break_minutes = 5  # 短休息时间（分钟）
        self.long_break_minutes = 15  # 长休息时间（分钟）
        self.pomodoros_before_long_break = 4  # 多少次番茄钟后进行长休息

        # 状态变量
        self.current_mode = "work"  # 当前模式: work, short_break, long_break
        self.current_state = "stopped"  # 当前状态: stopped, running, paused
        self.remaining_seconds = self.work_minutes * 60  # 剩余秒数
        self.total_seconds = self.work_minutes * 60  # 总秒数
        self.pomodoro_count = 0  # 完成的番茄钟数量
        self.is_long_break_next = False  # 下一次是否是长休息

        # 计时器
        self.timer = QTimer()
        self.timer.setInterval(1000)  # 1秒间隔
        self.timer.timeout.connect(self._update_timer)

        # 更新时间显示
        self._update_display()

    def _update_display(self):
        """更新时间显示文本"""
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.time_changed.emit(time_str)

    def _update_timer(self):
        """计时器更新回调"""
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self._update_display()
        else:
            self._on_timer_finished()

    def _on_timer_finished(self):
        """计时结束处理"""
        self.timer.stop()
        self.current_state = "stopped"
        self.state_changed.emit("stopped")

        # 发送完成信号
        if self.current_mode == "work":
            self.pomodoro_count += 1
            self.time_finished.emit(f"工作完成！已完成 {self.pomodoro_count} 个番茄钟")

            # 判断下一个休息类型
            if self.pomodoro_count % self.pomodoros_before_long_break == 0:
                self.is_long_break_next = True
                self.time_finished.emit(f"工作完成！接下来是长休息")
            else:
                self.is_long_break_next = False
                self.time_finished.emit(f"工作完成！接下来是短休息")
        else:
            mode_name = "长休息" if self.current_mode == "long_break" else "短休息"
            self.time_finished.emit(f"{mode_name}结束！接下来是工作")

    def start(self):
        """开始计时"""
        if self.current_state == "paused":
            # 从暂停状态继续
            self.current_state = "running"
        elif self.current_state == "stopped":
            # 从停止状态开始
            self.current_state = "running"
            # 如果是停止状态，重新设置时间
            self._set_time_for_current_mode()

        self.timer.start()
        self.state_changed.emit("running")

    def pause(self):
        """暂停计时"""
        if self.current_state == "running":
            self.timer.stop()
            self.current_state = "paused"
            self.state_changed.emit("paused")

    def reset(self):
        """重置计时器"""
        self.timer.stop()
        self.current_state = "stopped"
        self._set_time_for_current_mode()
        self._update_display()
        self.state_changed.emit("stopped")

    def skip(self):
        """跳过当前计时"""
        self.timer.stop()
        self.current_state = "stopped"

        # 切换到下一个模式
        if self.current_mode == "work":
            self.pomodoro_count += 1
            if self.pomodoro_count % self.pomodoros_before_long_break == 0:
                self.switch_to_long_break()
            else:
                self.switch_to_short_break()
        else:
            self.switch_to_work()

        self.state_changed.emit("stopped")

    def switch_to_work(self):
        """切换到工作模式"""
        self.current_mode = "work"
        self._set_time_for_current_mode()
        self.mode_changed.emit("work")
        self._update_display()

    def switch_to_short_break(self):
        """切换到短休息模式"""
        self.current_mode = "short_break"
        self._set_time_for_current_mode()
        self.mode_changed.emit("short_break")
        self._update_display()

    def switch_to_long_break(self):
        """切换到长休息模式"""
        self.current_mode = "long_break"
        self._set_time_for_current_mode()
        self.mode_changed.emit("long_break")
        self._update_display()

    def _set_time_for_current_mode(self):
        """根据当前模式设置时间"""
        if self.current_mode == "work":
            self.total_seconds = self.work_minutes * 60
        elif self.current_mode == "short_break":
            self.total_seconds = self.short_break_minutes * 60
        elif self.current_mode == "long_break":
            self.total_seconds = self.long_break_minutes * 60

        self.remaining_seconds = self.total_seconds

    def set_work_time(self, minutes):
        """设置工作时间"""
        self.work_minutes = minutes
        if self.current_mode == "work":
            self._set_time_for_current_mode()
            if self.current_state == "stopped":
                self._update_display()

    def set_short_break_time(self, minutes):
        """设置短休息时间"""
        self.short_break_minutes = minutes
        if self.current_mode == "short_break":
            self._set_time_for_current_mode()
            if self.current_state == "stopped":
                self._update_display()

    def set_long_break_time(self, minutes):
        """设置长休息时间"""
        self.long_break_minutes = minutes
        if self.current_mode == "long_break":
            self._set_time_for_current_mode()
            if self.current_state == "stopped":
                self._update_display()

    def get_current_mode(self):
        """获取当前模式"""
        return self.current_mode

    def get_current_state(self):
        """获取当前状态"""
        return self.current_state

    def get_pomodoro_count(self):
        """获取完成的番茄钟数量"""
        return self.pomodoro_count

    def get_remaining_seconds(self):
        """获取剩余秒数"""
        return self.remaining_seconds

    def get_total_seconds(self):
        """获取总秒数"""
        return self.total_seconds