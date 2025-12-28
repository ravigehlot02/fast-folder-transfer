@echo off
title Folder Transfer - Launcher

REM Go to backend folder
cd backend

REM Create virtual environment if not exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies quietly
echo Installing dependencies...
pip install --quiet fastapi uvicorn python-multipart

REM Start backend in a separate window
echo Starting backend server...
start "" uvicorn app:app --host 0.0.0.0 --port 8000 --reload

REM Wait a moment for server to start
timeout /t 2 /nobreak >nul

REM Open frontend in default browser (through the server)
echo Opening frontend...
start "" http://localhost:8000

echo Folder Transfer Launcher is running.
echo Backend is available at http://localhost:8000
echo Frontend will open in your browser.
pause
