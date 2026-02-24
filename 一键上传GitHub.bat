@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo      GitHub Auto Upload Tool (English Version)
echo ========================================================
echo.
echo [INFO] This script is in English to prevent encoding errors.
echo.

:: 1. Set Git path (try default installation path first)
set "GIT_EXE=C:\Program Files\Git\cmd\git.exe"
set "GH_EXE=C:\Program Files\GitHub CLI\gh.exe"

:: 2. Check if Git exists
if not exist "!GIT_EXE!" (
    echo [ERROR] Git not found at default location.
    echo Trying system PATH...
    set "GIT_EXE=git"
    where git >nul 2>nul
    if !ERRORLEVEL! NEQ 0 (
        echo [FATAL] Git is not installed or not in PATH.
        echo Please restart your computer if you just installed it.
        pause
        exit /b
    )
)

:: 3. Check if GitHub CLI exists
if not exist "!GH_EXE!" (
    echo [ERROR] GitHub CLI not found at default location.
    echo Trying system PATH...
    set "GH_EXE=gh"
    where gh >nul 2>nul
    if !ERRORLEVEL! NEQ 0 (
        echo [FATAL] GitHub CLI is not installed or not in PATH.
        echo Please restart your computer if you just installed it.
        pause
        exit /b
    )
)

echo [1/5] Initializing Git Repository...
if not exist .git (
    "!GIT_EXE!" init
    echo Repository initialized.
) else (
    echo Git repository already exists. Skipping init.
)

echo [2/5] Adding files to staging area...
"!GIT_EXE!" add .

echo [3/5] Committing changes...
"!GIT_EXE!" commit -m "Auto upload by script: Update docs and structure"

echo.
echo [4/5] GitHub Authentication
echo ========================================================
echo IMPORTANT INSTRUCTIONS:
echo 1. A browser window will open shortly.
echo 2. Login to your GitHub account and authorize.
echo 3. If a verification code is shown here, enter it in the browser.
echo ========================================================
echo.
pause
"!GH_EXE!" auth login --web

echo.
echo [5/5] Creating and Pushing to Remote Repository
set /p REPO_NAME="Enter repository name (Press Enter for 'pdf-to-word-monitor'): "
if "!REPO_NAME!"=="" set REPO_NAME=pdf-to-word-monitor

echo Creating repository '!REPO_NAME!'...
"!GH_EXE!" repo create !REPO_NAME! --private --source=. --remote=origin --push

if !ERRORLEVEL! EQU 0 (
    echo.
    echo ========================================================
    echo      SUCCESS! Project uploaded to GitHub.
    echo ========================================================
    echo URL: https://github.com/!REPO_NAME!
) else (
    echo.
    echo [WARNING] Upload might have failed or repo already exists.
    echo Please check the error messages above.
)

echo.
echo Press any key to exit...
pause
