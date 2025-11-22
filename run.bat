@echo off
echo ========================================
echo   Tourism Guide - Full Stack Launcher
echo ========================================
echo.

echo [1/3] Checking prerequisites...
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.11+ and try again.
    pause
    exit /b 1
)
echo   ✓ Python found

echo.
echo [2/3] Starting Backend Server...
cd backend
start "Tourism Backend" cmd /k "venv\Scripts\activate && python -m app.main"
echo   ✓ Backend starting on http://localhost:8000
echo   (Check the new terminal window)

timeout /t 5 /nobreak >nul

echo.
echo [3/3] Starting Frontend Server...
cd ..\frontend
start "Tourism Frontend" cmd /k "python -m http.server 8080"
echo   ✓ Frontend starting on http://localhost:8080

timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   ✨ Tourism Guide is Ready! ✨
echo ========================================
echo.
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:8080
echo   API Docs: http://localhost:8000/docs
echo.
echo Opening frontend in your browser...
start http://localhost:8080

echo.
echo Press any key to stop all servers...
pause >nul

echo.
echo Stopping servers...
taskkill /FI "WINDOWTITLE eq Tourism Backend*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Tourism Frontend*" /T /F >nul 2>&1

echo.
echo Servers stopped. Goodbye!
timeout /t 2 >nul
