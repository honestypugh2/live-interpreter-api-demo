@echo off
REM Start script for React Demo App (Simulated Mode - No Backend Required)

echo ==================================================
echo Azure Live Interpreter - Demo Mode (Simulated)
echo ==================================================
echo.

REM Check if we're in the react_app directory
if not exist "frontend\package.json" (
    echo Error: Please run this script from the src\react_app directory
    echo    cd src\react_app
    echo    start-demo.bat
    exit /b 1
)

REM Check Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Node.js is not installed
    echo    Please install Node.js 18 or higher: https://nodejs.org/
    exit /b 1
)

echo Node.js detected
echo.

REM Install frontend dependencies if needed
cd frontend
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
    echo.
)

echo ==================================================
echo Starting Demo Mode (No Backend Required)
echo ==================================================
echo.
echo Demo Features:
echo    - Simulated council meeting with pre-scripted dialogue
echo    - English - Spanish translation demo
echo    - No microphone or Azure API required
echo    - Perfect for demonstrations and training
echo.
echo Note: If port 5173 is in use, Vite will automatically
echo       choose the next available port (5174, 5175, etc.)
echo.
echo Press Ctrl+C to stop
echo ==================================================
echo.

REM Start frontend in demo mode
echo Starting Vite development server...
echo.
call npm run dev:demo
