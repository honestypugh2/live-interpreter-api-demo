@echo off
REM Azure Live Interpreter React App - Quick Start Script (Windows)
REM This script starts both the backend and frontend servers

setlocal enabledelayedexpansion

echo ========================================
echo Azure Live Interpreter - Quick Start
echo ========================================
echo.

REM Get script directory
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%..\..\"
set "BACKEND_DIR=%SCRIPT_DIR%backend"
set "FRONTEND_DIR=%SCRIPT_DIR%frontend"

REM Check if .env file exists
if not exist "%PROJECT_ROOT%.env" (
    echo [ERROR] .env file not found in project root
    echo Please create a .env file with your Azure Speech Service credentials
    echo.
    echo Example .env file:
    echo SPEECH_KEY=your_key_here
    echo SPEECH_REGION=eastus
    echo.
    pause
    exit /b 1
)

echo [OK] .env file found

REM Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed
    pause
    exit /b 1
)
echo [OK] Python found

REM Check Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed
    pause
    exit /b 1
)
echo [OK] Node.js found

REM Check npm
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] npm is not installed
    pause
    exit /b 1
)
echo [OK] npm found

echo.

REM Check backend dependencies
echo Checking backend dependencies...
python -c "import fastapi" >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARN] Backend dependencies not found. Installing...
    cd /d "%PROJECT_ROOT%"
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install backend dependencies
        pause
        exit /b 1
    )
    echo [OK] Backend dependencies installed
) else (
    echo [OK] Backend dependencies found
)

REM Check frontend dependencies
echo Checking frontend dependencies...
if not exist "%FRONTEND_DIR%\node_modules" (
    echo [WARN] Frontend dependencies not found. Installing...
    cd /d "%FRONTEND_DIR%"
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install frontend dependencies
        pause
        exit /b 1
    )
    echo [OK] Frontend dependencies installed
) else (
    echo [OK] Frontend dependencies found
)

echo.
echo ========================================
echo Starting servers...
echo ========================================
echo.

REM Start backend
echo Starting backend server...
cd /d "%BACKEND_DIR%"
start "Azure Interpreter Backend" /MIN cmd /c "python main.py > backend.log 2>&1"

REM Wait for backend to start
echo Waiting for backend to be ready...
timeout /t 5 /nobreak >nul

REM Check backend health
set "BACKEND_READY=0"
for /L %%i in (1,1,10) do (
    curl -s http://localhost:8000/health >nul 2>nul
    if !errorlevel! equ 0 (
        set "BACKEND_READY=1"
        goto :backend_ready
    )
    timeout /t 1 /nobreak >nul
)

:backend_ready
if !BACKEND_READY! equ 0 (
    echo [ERROR] Backend failed to start
    echo Check backend.log for errors
    type backend.log
    pause
    exit /b 1
)
echo [OK] Backend is ready (http://localhost:8000)

REM Start frontend
echo Starting frontend server...
cd /d "%FRONTEND_DIR%"
start "Azure Interpreter Frontend" cmd /c "npm run dev > frontend.log 2>&1"

REM Wait for frontend to start
echo Waiting for frontend to be ready...
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo All servers are running!
echo ========================================
echo.
echo Access the application:
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo Logs:
echo   Backend:  %BACKEND_DIR%\backend.log
echo   Frontend: %FRONTEND_DIR%\frontend.log
echo.
echo Press any key to open the application in your browser...
echo Close this window to stop all servers.
pause >nul

REM Open browser
start http://localhost:5173

echo.
echo Servers are running. Close this window to stop them.
pause
