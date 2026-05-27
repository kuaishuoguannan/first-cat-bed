@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   番茄时钟安装脚本 (Windows)
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✓ 检测到Python
python --version

REM 检查pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [警告] 未找到pip，尝试修复...
    python -m ensurepip --default-pip
)

echo.
echo 正在安装依赖...
echo （这可能需要几分钟，请耐心等待...）
echo.

REM 安装依赖
call python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple --no-warn-script-location
if errorlevel 1 (
    echo [错误] pip升级失败
    pause
    exit /b 1
)

echo.
echo 正在安装应用依赖...

call python -m pip install PyQt6 pyqt6-tools -i https://pypi.tuna.tsinghua.edu.cn/simple --no-warn-script-location
if errorlevel 1 (
    echo [警告] PyQt6安装失败，尝试其他方式...
    call python requirements_install.py
)

call python -m pip install pygame plyer psutil -i https://pypi.tuna.tsinghua.edu.cn/simple --no-warn-script-location
if errorlevel 1 (
    echo [警告] 可选依赖安装失败，应用部分功能可能受限
)

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 运行方式：
echo   1. 双击 run.py
echo   2. 或命令行运行: python run.py
echo   3. 或直接运行: python src/main.py
echo.
echo 功能特点：
echo   - 开始/暂停/重置计时器
echo   - 工作/短休息/长休息模式切换
echo   - 快捷键支持（空格、R、S）
echo   - 现代简约界面风格
echo.
pause