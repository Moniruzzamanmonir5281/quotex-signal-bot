#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
এক-ক্লিক ইনস্টলেশন স্ক্রিপ্ট (Windows)
সমস্ত ফাইল সেটআপ এবং নির্ভরতা ইনস্টল করে
"""

@echo off
CLS

echo ================================
echo Quotex Signal Bot - Setup
echo ================================
echo.

echo [1/3] Python version checking...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python first.
    pause
    exit /b 1
)
echo OK: Python is installed
echo.

echo [2/3] Installing dependencies...
python -m pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo OK: Dependencies installed
echo.

echo [3/3] Running setup script...
python setup.py
echo.

echo ================================
echo Setup completed successfully!
echo ================================
echo.
echo Next steps:
echo 1. Edit .env file with your credentials
echo 2. Run: python main.py
echo.
pause
