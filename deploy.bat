@echo off
REM Tourism Guide - Quick Deployment Script for Windows
REM This script helps you deploy to GitHub quickly

echo ========================================
echo   Tourism Guide - Quick Deploy
echo ========================================
echo.

REM Check if git is initialized
if not exist .git (
    echo Initializing Git repository...
    git init
    git branch -M main
)

REM Check if remote exists
git remote | findstr "origin" >nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Enter your GitHub repository URL:
    echo (e.g., https://github.com/username/tourism-guide.git)
    set /p repo_url="URL: "
    
    if "%repo_url%"=="" (
        echo ERROR: No URL provided. Exiting.
        pause
        exit /b 1
    )
    
    git remote add origin %repo_url%
    echo Remote added: %repo_url%
)

REM Add all files
echo.
echo Adding files to git...
git add .

REM Commit
echo.
set /p commit_msg="Commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Ready for deployment

git commit -m "%commit_msg%"

REM Push
echo.
echo Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo   Successfully pushed to GitHub!
echo ========================================
echo.
echo Next Steps:
echo   1. Go to https://render.com
echo   2. Sign in with GitHub
echo   3. New Web Service - Select your repository
echo   4. Follow DEPLOYMENT_GUIDE.md
echo.
echo Your code is ready to deploy!
echo.
pause
