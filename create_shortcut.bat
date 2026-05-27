@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   创建番茄时钟桌面快捷方式
echo ========================================
echo.

REM 获取桌面路径
for /f "tokens=2*" %%I in ('reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop 2^>nul') do set "desktop=%%J"

if "%desktop%"=="" (
    echo [警告] 无法获取桌面路径，使用默认路径
    set "desktop=%USERPROFILE%\Desktop"
)

echo 桌面路径: %desktop%
echo.

REM 检查Python路径
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查脚本文件
if not exist "E:\Cursor\first CC\run_simple.py" (
    echo [错误] 未找到run_simple.py，请确保在此目录运行
    pause
    exit /b 1
)

echo 创建快捷方式...

REM 创建VBS脚本创建快捷方式
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%temp%\create_link.vbs"
echo sLinkFile = "%desktop%\番茄时钟.lnk" >> "%temp%\create_link.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%temp%\create_link.vbs"
echo oLink.TargetPath = "%windir%\System32\cmd.exe" >> "%temp%\create_link.vbs"
echo oLink.Arguments = "/c cd /d "E:\Cursor\first CC" && python run_simple.py" >> "%temp%\create_link.vbs"
echo oLink.WorkingDirectory = "E:\Cursor\first CC" >> "%temp%\create_link.vbs"
echo oLink.IconLocation = "E:\Cursor\first CC\resources\icons\pomodoro.ico" >> "%temp%\create_link.vbs"
echo oLink.Save >> "%temp%\create_link.vbs"

REM 运行VBS脚本
cscript //nologo "%temp%\create_link.vbs"

if exist "%desktop%\番茄时钟.lnk" (
    echo.
    echo ✅ 成功创建桌面快捷方式！
    echo 位置: %desktop%\番茄时钟.lnk
    echo.
    echo 双击即可运行番茄时钟
) else (
    echo.
    echo ⚠️ 创建快捷方式失败，请手动创建：
    echo 1. 右键点击 run_simple.py
    echo 2. 选择"发送到" -> "桌面快捷方式"
    echo 3. 重命名为"番茄时钟"
)

echo.
echo ========================================
echo   运行方式
echo ========================================
echo.
echo 1. 双击桌面上的 "番茄时钟.lnk" (推荐)
echo 2. 或直接运行: python run_simple.py
echo.
echo 按任意键退出...
pause >nul