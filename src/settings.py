#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置管理模块
"""

import json
import os
from pathlib import Path


class Settings:
    """配置管理类"""

    DEFAULT_SETTINGS = {
        "work_minutes": 25,
        "short_break_minutes": 5,
        "long_break_minutes": 15,
        "pomodoros_before_long_break": 4,
        "enable_sounds": True,
        "enable_notifications": True,
        "auto_start_breaks": False,
        "auto_start_pomodoros": False,
        "theme": "light",
        "language": "zh_CN",
        "window_pos": {"x": 100, "y": 100},
        "window_size": {"width": 500, "height": 600},
        "always_on_top": False,
        "minimize_to_tray": True
    }

    def __init__(self, config_dir=None):
        """初始化配置"""
        if config_dir is None:
            # 默认配置目录：用户主目录下的 .pomodoro_clock
            user_home = Path.home()
            self.config_dir = user_home / ".pomodoro_clock"
        else:
            self.config_dir = Path(config_dir)

        # 确保配置目录存在
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # 配置文件路径
        self.config_file = self.config_dir / "settings.json"

        # 加载配置
        self.settings = self._load_settings()

    def _load_settings(self):
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # 合并默认配置和加载的配置
                    settings = self.DEFAULT_SETTINGS.copy()
                    settings.update(loaded_settings)
                    return settings
            except (json.JSONDecodeError, IOError) as e:
                print(f"配置文件加载失败，使用默认配置: {e}")
                return self.DEFAULT_SETTINGS.copy()
        else:
            # 配置文件不存在，使用默认配置并保存
            default_settings = self.DEFAULT_SETTINGS.copy()
            self._save_settings(default_settings)
            return default_settings

    def _save_settings(self, settings):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"配置文件保存失败: {e}")
            return False

    def save(self):
        """保存当前配置"""
        return self._save_settings(self.settings)

    def get(self, key, default=None):
        """获取配置项"""
        return self.settings.get(key, default)

    def set(self, key, value):
        """设置配置项"""
        self.settings[key] = value
        return True

    def get_work_minutes(self):
        """获取工作时间（分钟）"""
        return self.get("work_minutes", 25)

    def set_work_minutes(self, minutes):
        """设置工作时间（分钟）"""
        minutes = int(minutes)
        if 1 <= minutes <= 120:  # 限制在1-120分钟之间
            return self.set("work_minutes", minutes)
        return False

    def get_short_break_minutes(self):
        """获取短休息时间（分钟）"""
        return self.get("short_break_minutes", 5)

    def set_short_break_minutes(self, minutes):
        """设置短休息时间（分钟）"""
        minutes = int(minutes)
        if 1 <= minutes <= 30:  # 限制在1-30分钟之间
            return self.set("short_break_minutes", minutes)
        return False

    def get_long_break_minutes(self):
        """获取长休息时间（分钟）"""
        return self.get("long_break_minutes", 15)

    def set_long_break_minutes(self, minutes):
        """设置长休息时间（分钟）"""
        minutes = int(minutes)
        if 5 <= minutes <= 60:  # 限制在5-60分钟之间
            return self.set("long_break_minutes", minutes)
        return False

    def get_pomodoros_before_long_break(self):
        """获取多少次番茄钟后进行长休息"""
        return self.get("pomodoros_before_long_break", 4)

    def set_pomodoros_before_long_break(self, count):
        """设置多少次番茄钟后进行长休息"""
        count = int(count)
        if 1 <= count <= 10:  # 限制在1-10次之间
            return self.set("pomodoros_before_long_break", count)
        return False

    def is_sound_enabled(self):
        """是否启用声音"""
        return self.get("enable_sounds", True)

    def enable_sounds(self, enabled=True):
        """启用/禁用声音"""
        return self.set("enable_sounds", enabled)

    def is_notification_enabled(self):
        """是否启用通知"""
        return self.get("enable_notifications", True)

    def enable_notifications(self, enabled=True):
        """启用/禁用通知"""
        return self.set("enable_notifications", enabled)

    def is_auto_start_breaks(self):
        """是否自动开始休息"""
        return self.get("auto_start_breaks", False)

    def set_auto_start_breaks(self, enabled=True):
        """设置是否自动开始休息"""
        return self.set("auto_start_breaks", enabled)

    def is_auto_start_pomodoros(self):
        """是否自动开始下一个番茄钟"""
        return self.get("auto_start_pomodoros", False)

    def set_auto_start_pomodoros(self, enabled=True):
        """设置是否自动开始下一个番茄钟"""
        return self.set("auto_start_pomodoros", enabled)

    def get_theme(self):
        """获取主题"""
        return self.get("theme", "light")

    def set_theme(self, theme):
        """设置主题"""
        if theme in ["light", "dark", "blue"]:
            return self.set("theme", theme)
        return False

    def get_language(self):
        """获取语言"""
        return self.get("language", "zh_CN")

    def set_language(self, language):
        """设置语言"""
        if language in ["zh_CN", "en_US"]:
            return self.set("language", language)
        return False

    def get_window_position(self):
        """获取窗口位置"""
        return self.get("window_pos", {"x": 100, "y": 100})

    def set_window_position(self, x, y):
        """设置窗口位置"""
        return self.set("window_pos", {"x": x, "y": y})

    def get_window_size(self):
        """获取窗口大小"""
        return self.get("window_size", {"width": 500, "height": 600})

    def set_window_size(self, width, height):
        """设置窗口大小"""
        return self.set("window_size", {"width": width, "height": height})

    def is_always_on_top(self):
        """是否始终在最前"""
        return self.get("always_on_top", False)

    def set_always_on_top(self, enabled=True):
        """设置是否始终在最前"""
        return self.set("always_on_top", enabled)

    def is_minimize_to_tray(self):
        """是否最小化到托盘"""
        return self.get("minimize_to_tray", True)

    def set_minimize_to_tray(self, enabled=True):
        """设置是否最小化到托盘"""
        return self.set("minimize_to_tray", enabled)

    def reset_to_defaults(self):
        """重置为默认配置"""
        self.settings = self.DEFAULT_SETTINGS.copy()
        return self.save()


# 全局配置实例
_g_settings = None


def get_settings(config_dir=None):
    """获取全局配置实例"""
    global _g_settings
    if _g_settings is None:
        _g_settings = Settings(config_dir)
    return _g_settings


if __name__ == "__main__":
    # 测试配置管理
    settings = get_settings()
    print(f"工作时间: {settings.get_work_minutes()} 分钟")
    print(f"短休息时间: {settings.get_short_break_minutes()} 分钟")
    print(f"长休息时间: {settings.get_long_break_minutes()} 分钟")
    print(f"语言: {settings.get_language()}")