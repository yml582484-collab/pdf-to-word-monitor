@echo off
setlocal enabledelayedexpansion

:: Switch to English mode to avoid encoding issues
echo ========================================
echo      PDF to Word Monitor (Foreground)
echo ========================================
echo.
echo [INFO] Starting monitor...
echo [INFO] Watch Directory: %~dp0
echo [TIP]  Just drag and drop PDF files here!
echo.
echo Press Ctrl+C to stop monitoring.
echo.

cd /d "%~dp0"
python pdf_monitor.py
pause
