@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d C:\Users\jiawa\ai-daily-report
python main.py weekly >> logs\run.log 2>&1
