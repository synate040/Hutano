@echo off
echo.
echo ========================================
echo  HUTANO Hospital System - Quick Setup
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Setting up database...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Database setup failed
    pause
    exit /b 1
)

echo Running setup script...
python setup.py
if errorlevel 1 (
    echo ERROR: Setup script failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo To start the server:
echo   python manage.py runserver
echo.
echo Then open: http://127.0.0.1:8000/core/data-upload/
echo.
pause
