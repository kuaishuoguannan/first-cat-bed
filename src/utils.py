#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
工具函数模块
"""

import sys
import os
import json
import time
import subprocess
import platform
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

# 导入第三方库（如果有的话）
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


def get_resource_path(relative_path: str) -> str:
    """获取资源文件的绝对路径"""
    # 如果是打包后的可执行文件
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # PyInstaller打包后的路径
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    resource_dir = os.path.join(base_path, "resources")
    full_path = os.path.join(resource_dir, relative_path)

    # 如果不存在，尝试在当前目录查找
    if not os.path.exists(full_path):
        # 尝试在当前工作目录的resources文件夹查找
        current_dir = os.getcwd()
        full_path = os.path.join(current_dir, "resources", relative_path)

    return full_path


def format_time(seconds: int) -> str:
    """格式化时间（秒 -> MM:SS）"""
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"


def format_time_long(seconds: int) -> str:
    """格式化长时间（秒 -> HH:MM:SS）"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
    else:
        return f"{minutes:02d}:{remaining_seconds:02d}"


def format_time_human(seconds: int) -> str:
    """人性化时间格式化"""
    if seconds < 60:
        return f"{seconds}秒"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        if remaining_seconds == 0:
            return f"{minutes}分钟"
        else:
            return f"{minutes}分钟{remaining_seconds}秒"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if minutes == 0:
            return f"{hours}小时"
        else:
            return f"{hours}小时{minutes}分钟"


def get_system_info() -> Dict[str, Any]:
    """获取系统信息"""
    info = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.architecture()[0],
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }

    if HAS_PSUTIL:
        try:
            info["cpu_count"] = psutil.cpu_count()
            info["memory_total"] = psutil.virtual_memory().total
            info["memory_available"] = psutil.virtual_memory().available
        except Exception:
            pass

    return info


def play_sound(sound_file: str) -> bool:
    """播放声音文件"""
    try:
        sound_path = get_resource_path(sound_file)

        if not os.path.exists(sound_path):
            print(f"声音文件不存在: {sound_path}")
            return False

        # 根据平台选择播放方式
        system = platform.system()

        if system == "Windows":
            import winsound
            winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            return True
        elif system == "Darwin":  # macOS
            subprocess.run(["afplay", sound_path], check=False)
            return True
        elif system == "Linux":
            try:
                # 尝试使用pygame播放
                import pygame
                pygame.mixer.init()
                pygame.mixer.Sound(sound_path).play()
                return True
            except ImportError:
                # 使用系统命令
                subprocess.run(["aplay", sound_path], check=False)
                return True
        else:
            print(f"不支持的操作系统: {system}")
            return False

    except Exception as e:
        print(f"播放声音失败: {e}")
        return False


def show_system_notification(title: str, message: str) -> bool:
    """显示系统通知"""
    try:
        system = platform.system()

        if system == "Windows":
            # Windows: 使用win10toast或plyer
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=3)
                return True
            except ImportError:
                # 尝试使用plyer
                try:
                    from plyer import notification
                    notification.notify(
                        title=title,
                        message=message,
                        timeout=3
                    )
                    return True
                except ImportError:
                    pass

        elif system == "Darwin":  # macOS
            try:
                import subprocess
                cmd = f'''
                osascript -e 'display notification "{message}" with title "{title}"'
                '''
                subprocess.run(cmd, shell=True, check=False)
                return True
            except Exception:
                pass

        elif system == "Linux":
            # Linux: 使用notify-send命令
            try:
                subprocess.run(
                    ["notify-send", title, message, "-t", "3000"],
                    check=False
                )
                return True
            except FileNotFoundError:
                pass

        # 如果不支持显示通知，至少打印到控制台
        print(f"[通知] {title}: {message}")
        return True

    except Exception as e:
        print(f"显示通知失败: {e}")
        return False


def create_resource_folders():
    """创建资源文件夹结构"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    resource_dir = os.path.join(base_dir, "resources")
    folders = ["sounds", "icons", "themes", "data"]

    for folder in folders:
        folder_path = os.path.join(resource_dir, folder)
        os.makedirs(folder_path, exist_ok=True)

    # 创建默认声音文件
    create_default_sound_file()


def create_default_sound_file():
    """创建默认的提醒声音"""
    try:
        import wave
        import struct
        import math

        sound_path = get_resource_path("sounds/ding.wav")

        if os.path.exists(sound_path):
            return

        # 创建简单的叮铃声
        sample_rate = 44100
        duration = 1.0  # 1秒
        frequency = 880  # A5音符

        num_samples = int(sample_rate * duration)

        with wave.open(sound_path, 'w') as wav_file:
            wav_file.setnchannels(1)  # 单声道
            wav_file.setsampwidth(2)  # 16位
            wav_file.setframerate(sample_rate)

            for i in range(num_samples):
                # 创建正弦波，添加淡出效果
                sample = 0.5 * math.sin(2 * math.pi * frequency * i / sample_rate)
                fade = 1.0 - (i / num_samples)  # 线性淡出
                sample *= fade

                # 转换为16位整数
                int_sample = int(sample * 32767)
                wav_file.writeframes(struct.pack('<h', int_sample))

        print(f"已创建默认声音文件: {sound_path}")

    except Exception as e:
        print(f"创建默认声音文件失败: {e}")
        # 创建一个空的占位符文件
        try:
            placeholder_path = get_resource_path("sounds/ding.wav")
            with open(placeholder_path, 'wb') as f:
                f.write(b'')
        except Exception:
            pass


def ensure_single_instance(app_name: str) -> bool:
    """确保应用只有一个实例运行"""
    import socket
    import sys

    # 尝试绑定到一个特定的端口
    lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lock_port = 18861  # 一个随机的端口号

    try:
        lock_socket.bind(('localhost', lock_port))
        return True  # 绑定成功，这是第一个实例
    except socket.error:
        # 绑定失败，已经有实例在运行
        print(f"应用 '{app_name}' 已经在运行中")
        return False


def calculate_productivity_score(work_time: int, break_time: int, pomodoro_count: int) -> float:
    """计算生产力分数"""
    if work_time == 0:
        return 0.0

    # 工作时间比例分数（0-60分）
    time_score = min(work_time / (25 * 60 * 8) * 60, 60)  # 8小时工作制的60%

    # 番茄钟数量分数（0-30分）
    pomodoro_score = min(pomodoro_count / 16 * 30, 30)  # 16个番茄钟为满分

    # 休息平衡分数（0-10分）
    if work_time > 0:
        break_ratio = break_time / work_time
        if 0.15 <= break_ratio <= 0.25:  # 理想的休息比例是15-25%
            break_score = 10
        elif 0.1 <= break_ratio <= 0.3:  # 可接受的范围
            break_score = 7
        else:
            break_score = 3
    else:
        break_score = 5

    total_score = time_score + pomodoro_score + break_score

    # 标准化到0-100
    normalized_score = min(total_score * 100 / 100, 100)

    return round(normalized_score, 1)


def format_date_chinese(date_obj: datetime.date) -> str:
    """将日期格式化为中文格式"""
    return date_obj.strftime("%Y年%m月%d日")


def format_datetime_chinese(datetime_obj: datetime) -> str:
    """将日期时间格式化为中文格式"""
    return datetime_obj.strftime("%Y年%m月%d日 %H:%M:%S")


def get_weekday_chinese(date_obj: datetime.date) -> str:
    """获取中文星期几"""
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return weekdays[date_obj.weekday()]


def is_work_hours() -> bool:
    """判断当前是否在工作时间（9:00-18:00）"""
    now = datetime.now()
    return 9 <= now.hour < 18


def validate_time_input(minutes: str) -> Optional[int]:
    """验证时间输入，返回分钟数或None"""
    try:
        minutes_int = int(minutes)
        if 1 <= minutes_int <= 120:
            return minutes_int
        return None
    except ValueError:
        return None


def get_app_version() -> str:
    """获取应用版本号"""
    try:
        # 尝试从项目配置文件中读取版本号
        import toml
        pyproject_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "pyproject.toml"
        )
        if os.path.exists(pyproject_path):
            config = toml.load(pyproject_path)
            return config.get("project", {}).get("version", "1.0.0")
    except Exception:
        pass

    # 默认版本
    return "1.0.0"


if __name__ == "__main__":
    # 测试工具函数
    print(f"当前时间: {format_time(150)}")  # 2:30
    print(f"长时间: {format_time_long(7323)}")  # 2:02:03
    print(f"人性化时间: {format_time_human(7323)}")  # 2小时2分钟

    # 测试系统信息
    sys_info = get_system_info()
    print(f"系统信息: {sys_info['platform']} {sys_info['platform_release']}")

    # 测试生产力分数计算
    score = calculate_productivity_score(4 * 25 * 60, 4 * 5 * 60, 4)
    print(f"生产力分数: {score}")