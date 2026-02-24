@echo off
chcp 65001 > nul
echo ========================================
echo      PDF转Word自动监控工具
echo ========================================
echo.
echo 正在启动监控...
echo 监控目录: %~dp0
echo (请将PDF文件拖入此文件夹即可自动转换)
echo 按 Ctrl+C 停止监控
echo.
cd /d "%~dp0"
python pdf_monitor.py