@echo off
chcp 65001 > nul
setlocal

echo ========================================
echo      GitHub 自动配置与上传工具
echo ========================================
echo.

:: 设置 Git 和 GitHub CLI 的可能路径
set "PATH=%PATH%;C:\Program Files\Git\cmd;C:\Program Files\GitHub CLI"

:: 检查 Git 是否可用
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未找到 Git，请确保 Git 已正确安装。
    echo 您可以尝试重启电脑让环境变量生效。
    pause
    exit /b
)

:: 检查 GitHub CLI 是否可用
where gh >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未找到 GitHub CLI (gh)，请确保已安装。
    echo 您可以尝试重启电脑让环境变量生效。
    pause
    exit /b
)

echo [1/5] 初始化 Git 仓库...
if not exist .git (
    git init
    echo 仓库初始化完成。
) else (
    echo 仓库已存在，跳过初始化。
)

echo [2/5] 添加文件到暂存区...
git add .

echo [3/5] 提交更改...
git commit -m "Initial commit: PDF转Word自动监控工具 (v1.0)"

echo.
echo [4/5] GitHub 登录验证
echo 请在浏览器中按照提示完成登录...
gh auth login --web

echo.
echo [5/5] 创建远程仓库并上传代码
:: 尝试创建私有仓库（如果需要公开，去掉 --private）
set /p REPO_NAME="请输入要在 GitHub 上创建的仓库名称 (默认: pdf-to-word-monitor): "
if "%REPO_NAME%"=="" set REPO_NAME=pdf-to-word-monitor

gh repo create %REPO_NAME% --private --source=. --remote=origin --push

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo      恭喜！项目已成功上传到 GitHub
    echo ========================================
    echo 仓库地址: https://github.com/%USERNAME%/%REPO_NAME%
) else (
    echo.
    echo [警告] 上传过程中可能遇到问题，请检查错误信息。
    echo 如果提示仓库已存在，请忽略此错误。
)

echo.
pause
