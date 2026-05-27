# Pomodoro Clock 番茄时钟

一个现代化的桌面番茄时钟应用，采用 Python + PyQt6 技术栈。

## 功能特性

✅ **核心计时功能**
- 工作计时（默认25分钟）
- 短休息计时（默认5分钟）
- 长休息计时（默认15分钟）

✅ **控制功能**
- 开始/暂停/继续
- 重置计时器
- 切换工作/休息模式
- 跳过当前计时

✅ **提醒功能**
- 结束时响铃提醒
- 系统通知弹窗
- 托盘图标闪烁

✅ **数据统计**
- 番茄钟计数
- 每日/每周统计
- 历史记录图表
- 最长专注记录

✅ **自定义设置**
- 工作时间调整
- 休息时间调整
- 提醒声音选择
- 主题颜色切换

✅ **高级功能**
- 系统托盘常驻
- 全局快捷键
- 任务标签管理
- 专注免打扰模式

## 技术栈

- **Python 3.8+**
- **PyQt6** - GUI框架
- **SQLite** - 数据存储
- **PyGame** - 音频播放
- **PyInstaller** - 打包工具

## 项目结构

```
pomodoro-clock/
├── src/                    # 源代码
│   ├── __init__.py
│   ├── main.py            # 程序入口
│   ├── timer.py           # 计时器逻辑
│   ├── ui.py              # 界面组件
│   ├── settings.py        # 配置管理
│   ├── database.py        # 数据库操作
│   └── utils.py           # 工具函数
├── resources/             # 资源文件
│   ├── sounds/           # 音频文件
│   ├── icons/            # 图标文件
│   └── themes/           # 主题文件
├── tests/                # 测试文件
├── docs/                 # 文档
├── requirements.txt      # 依赖列表
├── pyproject.toml       # 项目配置
└── README.md            # 项目说明
```

## 安装与运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行应用
```bash
python src/main.py
```

### 3. 打包可执行文件（可选）
```bash
pyinstaller --onefile --windowed --icon=resources/icons/pomodoro.ico src/main.py
```

## 使用说明

1. **启动应用**：运行 `python src/main.py`
2. **设置时间**：根据需要调整工作和休息时间
3. **开始计时**：点击"开始"按钮或按空格键
4. **暂停/继续**：需要暂停时可点击"暂停"按钮
5. **结束提醒**：计时结束后会有声音和通知提醒
6. **查看统计**：在主界面查看当天的番茄钟完成情况

## 跨平台支持

- **Windows**：完整支持
- **macOS**：完整支持
- **Linux**：完整支持（需安装相关依赖）

## 快捷键

- **空格键**：开始/暂停
- **R键**：重置计时器
- **S键**：跳过当前计时
- **Esc键**：最小化到托盘
- **Ctrl+Q**：退出应用

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。