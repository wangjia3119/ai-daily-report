@echo off
chcp 65001 >nul
echo ============================================
echo  配置 Windows 任务计划程序
echo ============================================
echo.

set SCRIPT_DIR=C:\Users\jiawa\ai-daily-report

echo [1/2] 创建每日日报任务（周一至周四 08:00）...
schtasks /create /tn "AI日报-每日" /tr "%SCRIPT_DIR%\run_daily.bat" /sc WEEKLY /d MON,TUE,WED,THU /st 08:00 /f
if %errorlevel% equ 0 (
    echo   ✓ 每日任务创建成功
) else (
    echo   × 失败，请以管理员身份运行此脚本
)

echo.
echo [2/2] 创建每周周报任务（周五 08:00）...
schtasks /create /tn "AI周报-每周五" /tr "%SCRIPT_DIR%\run_weekly.bat" /sc WEEKLY /d FRI /st 08:00 /f
if %errorlevel% equ 0 (
    echo   ✓ 周报任务创建成功
) else (
    echo   × 失败，请以管理员身份运行此脚本
)

echo.
echo ============================================
echo  任务计划配置完成！
echo  可在"任务计划程序"中查看和修改时间
echo  运行路径: 任务计划程序库 → AI日报-每日 / AI周报-每周五
echo ============================================
echo.
pause
