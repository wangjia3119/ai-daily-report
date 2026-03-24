@echo off
chcp 65001 >nul
echo ============================================
echo  AI 日报自动化 - 一键安装
echo ============================================
echo.

echo [1/3] 安装 Python 依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 错误：pip install 失败，请检查 Python 环境
    pause
    exit /b 1
)

echo.
echo [2/3] 复制配置文件...
if not exist .env (
    copy .env.example .env
    echo 已创建 .env 文件，请用记事本打开并填写 API Key
) else (
    echo .env 文件已存在，跳过
)

echo.
echo [3/3] 初始化 Git 仓库...
if not exist .git (
    git init
    git add .gitignore requirements.txt templates\ *.py *.bat *.md
    git commit -m "init: AI 日报自动化项目初始化"
    echo Git 初始化完成
    echo.
    echo 下一步：
    echo   1. 在 GitHub 创建仓库 ai-daily-report
    echo   2. 运行: git remote add origin https://github.com/你的用户名/ai-daily-report.git
    echo   3. 运行: git push -u origin main
    echo   4. 在 GitHub 仓库设置中开启 GitHub Pages（选 main 分支 /output 目录）
) else (
    echo Git 仓库已存在，跳过
)

echo.
echo ============================================
echo  安装完成！
echo  请编辑 .env 文件填写以下内容：
echo    ANTHROPIC_API_KEY  - Claude API Key
echo    TAVILY_API_KEY     - Tavily API Key（免费）
echo    SERVER_CHAN_KEY    - Server酱 Key（免费，微信推送）
echo    GITHUB_PAGES_URL   - GitHub Pages 地址
echo ============================================
echo.
pause
