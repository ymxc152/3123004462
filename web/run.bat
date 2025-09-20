@echo off
chcp 65001 >nul
title Paper Check System - Auto Setup

echo ============================================================
echo Paper Check System - Auto Setup and Launch
echo ============================================================
echo.

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo [OK] Python is installed

:: Check if dependencies are already installed
python -c "import flask, numpy, jieba" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    python -m pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)

echo.
echo ============================================================
echo Starting Web Application...
echo Access URL: http://localhost:5000
echo Press Ctrl+C to stop service
echo ============================================================
echo.

:: Start the application with quiet output
python -W ignore app.py

:: If we get here, the app stopped
echo.
echo [INFO] Web application stopped
pause
