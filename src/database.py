#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据库管理模块
"""

import sqlite3
import json
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class Database:
    """数据库管理类"""

    def __init__(self, db_path=None):
        """初始化数据库"""
        if db_path is None:
            # 默认数据库路径：用户配置目录下的 pomodoro.db
            user_home = Path.home()
            config_dir = user_home / ".pomodoro_clock"
            config_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = config_dir / "pomodoro.db"
        else:
            self.db_path = Path(db_path)

        # 初始化数据库
        self._init_database()

    def _init_database(self):
        """初始化数据库表结构"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # 创建番茄钟记录表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pomodoros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time TIMESTAMP NOT NULL,
                    end_time TIMESTAMP NOT NULL,
                    duration INTEGER NOT NULL,  -- 单位：秒
                    mode TEXT NOT NULL,  -- work, short_break, long_break
                    rating INTEGER,  -- 评分 1-5
                    notes TEXT,     -- 备注
                    tags TEXT       -- 标签，JSON格式存储
                )
            """)

            # 创建每日统计表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_stats (
                    date DATE PRIMARY KEY,
                    total_pomodoros INTEGER DEFAULT 0,
                    total_work_time INTEGER DEFAULT 0,  -- 单位：秒
                    total_break_time INTEGER DEFAULT 0,  -- 单位：秒
                    completed_tasks INTEGER DEFAULT 0,
                    notes TEXT
                )
            """)

            # 创建设置表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS app_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)

            # 创建索引
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pomodoros_start_time ON pomodoros(start_time)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pomodoros_date ON pomodoros(DATE(start_time))")

            conn.commit()

    def add_pomodoro(self, start_time: datetime, end_time: datetime,
                     mode: str, rating: int = None, notes: str = None,
                     tags: List[str] = None) -> int:
        """添加一个番茄钟记录"""
        duration = int((end_time - start_time).total_seconds())

        tags_json = json.dumps(tags) if tags else None

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pomodoros
                (start_time, end_time, duration, mode, rating, notes, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (start_time.isoformat(), end_time.isoformat(),
                  duration, mode, rating, notes, tags_json))

            pomodoro_id = cursor.lastrowid

            # 更新每日统计
            self._update_daily_stats(date.fromisoformat(start_time.date().isoformat()), mode, duration)

            conn.commit()

        return pomodoro_id

    def _update_daily_stats(self, stat_date: date, mode: str, duration: int):
        """更新每日统计"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # 检查该日期是否已有记录
            cursor.execute("SELECT * FROM daily_stats WHERE date = ?", (stat_date.isoformat(),))
            existing = cursor.fetchone()

            if existing:
                # 更新现有记录
                if mode == "work":
                    cursor.execute("""
                        UPDATE daily_stats SET
                        total_pomodoros = total_pomodoros + 1,
                        total_work_time = total_work_time + ?
                        WHERE date = ?
                    """, (duration, stat_date.isoformat()))
                else:
                    cursor.execute("""
                        UPDATE daily_stats SET
                        total_break_time = total_break_time + ?
                        WHERE date = ?
                    """, (duration, stat_date.isoformat()))
            else:
                # 插入新记录
                if mode == "work":
                    cursor.execute("""
                        INSERT INTO daily_stats
                        (date, total_pomodoros, total_work_time)
                        VALUES (?, 1, ?)
                    """, (stat_date.isoformat(), duration))
                else:
                    cursor.execute("""
                        INSERT INTO daily_stats
                        (date, total_break_time)
                        VALUES (?, ?)
                    """, (stat_date.isoformat(), duration))

            conn.commit()

    def get_today_stats(self) -> Dict:
        """获取今日统计"""
        today = date.today()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM daily_stats WHERE date = ?", (today.isoformat(),))
            row = cursor.fetchone()

        if row:
            return {
                "date": row[0],
                "total_pomodoros": row[1] or 0,
                "total_work_time": row[2] or 0,
                "total_break_time": row[3] or 0,
                "completed_tasks": row[4] or 0,
                "notes": row[5]
            }
        else:
            return {
                "date": today.isoformat(),
                "total_pomodoros": 0,
                "total_work_time": 0,
                "total_break_time": 0,
                "completed_tasks": 0,
                "notes": None
            }

    def get_weekly_stats(self) -> Dict:
        """获取本周统计"""
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())  # 周一开始

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    SUM(total_pomodoros) as total_pomodoros,
                    SUM(total_work_time) as total_work_time,
                    SUM(total_break_time) as total_break_time,
                    SUM(completed_tasks) as completed_tasks
                FROM daily_stats
                WHERE date >= ?
            """, (start_of_week.isoformat(),))

            row = cursor.fetchone()

        return {
            "week_start": start_of_week.isoformat(),
            "total_pomodoros": row[0] or 0,
            "total_work_time": row[1] or 0,
            "total_break_time": row[2] or 0,
            "completed_tasks": row[3] or 0
        }

    def get_monthly_stats(self, year: int = None, month: int = None) -> Dict:
        """获取月度统计"""
        if year is None or month is None:
            today = date.today()
            year, month = today.year, today.month

        import calendar
        start_date = date(year, month, 1)
        end_date = date(year, month, calendar.monthrange(year, month)[1])

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    SUM(total_pomodoros) as total_pomodoros,
                    SUM(total_work_time) as total_work_time,
                    SUM(total_break_time) as total_break_time,
                    SUM(completed_tasks) as completed_tasks
                FROM daily_stats
                WHERE date >= ? AND date <= ?
            """, (start_date.isoformat(), end_date.isoformat()))

            row = cursor.fetchone()

        return {
            "year": year,
            "month": month,
            "total_pomodoros": row[0] or 0,
            "total_work_time": row[1] or 0,
            "total_break_time": row[2] or 0,
            "completed_tasks": row[3] or 0
        }

    def get_pomodoro_history(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """获取番茄钟历史记录"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM pomodoros
                ORDER BY start_time DESC
                LIMIT ? OFFSET ?
            """, (limit, offset))

            rows = cursor.fetchall()

        result = []
        for row in rows:
            pomodoro = dict(row)
            # 解析JSON格式的标签
            if pomodoro['tags']:
                pomodoro['tags'] = json.loads(pomodoro['tags'])
            result.append(pomodoro)

        return result

    def get_pomodoro_count_by_date_range(self, start_date: date, end_date: date) -> Dict[date, int]:
        """获取指定日期范围内的番茄钟数量"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT DATE(start_time) as date, COUNT(*) as count
                FROM pomodoros
                WHERE DATE(start_time) >= ? AND DATE(start_time) <= ?
                AND mode = 'work'
                GROUP BY DATE(start_time)
                ORDER BY date
            """, (start_date.isoformat(), end_date.isoformat()))

            rows = cursor.fetchall()

        return {date.fromisoformat(row[0]): row[1] for row in rows}

    def delete_pomodoro(self, pomodoro_id: int) -> bool:
        """删除番茄钟记录"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pomodoros WHERE id = ?", (pomodoro_id,))
            conn.commit()
            return cursor.rowcount > 0

    def update_pomodoro(self, pomodoro_id: int, rating: int = None,
                       notes: str = None, tags: List[str] = None) -> bool:
        """更新番茄钟记录"""
        updates = []
        params = []

        if rating is not None:
            updates.append("rating = ?")
            params.append(rating)

        if notes is not None:
            updates.append("notes = ?")
            params.append(notes)

        if tags is not None:
            updates.append("tags = ?")
            params.append(json.dumps(tags))

        if not updates:
            return False

        params.append(pomodoro_id)

        sql = f"UPDATE pomodoros SET {', '.join(updates)} WHERE id = ?"

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.rowcount > 0

    def get_app_setting(self, key: str, default: str = "") -> str:
        """获取应用设置"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM app_settings WHERE key = ?", (key,))
            row = cursor.fetchone()

        return row[0] if row else default

    def set_app_setting(self, key: str, value: str) -> bool:
        """设置应用设置"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO app_settings (key, value)
                VALUES (?, ?)
            """, (key, value))
            conn.commit()
            return True

    def backup_database(self, backup_path: str) -> bool:
        """备份数据库"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            return True
        except Exception as e:
            print(f"数据库备份失败: {e}")
            return False

    def reset_database(self):
        """重置数据库（清空所有数据）"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pomodoros")
            cursor.execute("DELETE FROM daily_stats")
            cursor.execute("DELETE FROM app_settings")
            conn.commit()


# 全局数据库实例
_g_database = None


def get_database(db_path=None):
    """获取全局数据库实例"""
    global _g_database
    if _g_database is None:
        _g_database = Database(db_path)
    return _g_database


if __name__ == "__main__":
    # 测试数据库功能
    db = get_database()
    print("数据库测试:")

    # 测试今日统计
    today_stats = db.get_today_stats()
    print(f"今日统计: {today_stats}")

    # 测试本周统计
    weekly_stats = db.get_weekly_stats()
    print(f"本周统计: {weekly_stats}")