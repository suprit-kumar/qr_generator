@echo off
REM QR Code Generator - Windows Batch File for Quick Start

REM Ensure the script runs from its own directory
cd /d "%~dp0"

echo.
echo ================================================
echo  QR Code Generator - Quick Start
echo ================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        echo Make sure Python is installed and in your PATH
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Upgrading pip, setuptools, and wheel...
    python -m pip install --upgrade pip setuptools wheel
    if errorlevel 1 (
        echo Error: Failed to upgrade pip tools
        pause
        exit /b 1
    )

    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Create necessary directories
if not exist "static\uploads" mkdir static\uploads
if not exist "static\generated_qr" mkdir static\generated_qr

REM Set Flask environment
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=1

echo.
echo ================================================
echo  Starting QR Code Generator...
echo ================================================
echo.
echo Application will be available at:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run Flask application
python app.py

pause
