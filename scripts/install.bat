@echo off
REM Code Quality & Security Audit System - Windows Installation Script

echo 🔍 Code Quality & Security Audit System - Installation
echo ==================================================

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python installation found

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📥 Installing Python dependencies...
pip install -r requirements.txt

REM Check if Ollama is installed
where ollama >nul 2>&1
if errorlevel 1 (
    echo 🤖 Ollama not found. Please install Ollama manually:
    echo 1. Download from https://ollama.ai/download
    echo 2. Install and restart this script
    pause
    exit /b 1
) else (
    echo ✅ Ollama is already installed
)

REM Start Ollama (if not running)
echo 🚀 Starting Ollama service...
start /B ollama serve

REM Wait for Ollama to be ready
echo ⏳ Waiting for Ollama to be ready...
timeout /t 10 /nobreak >nul

REM Pull required models
echo 📥 Downloading AI models (this may take a while)...
start /B ollama pull deepseek-coder:6.7b
start /B ollama pull deepseek-r1:1.5b
start /B ollama pull deepscaler

echo ⏳ Models are downloading in background...

REM Create sample project for testing
echo 📁 Creating sample project...
mkdir sample_project 2>nul
echo import os > sample_project\vulnerable_app.py
echo import sqlite3 >> sample_project\vulnerable_app.py
echo. >> sample_project\vulnerable_app.py
echo # Vulnerable code examples for testing >> sample_project\vulnerable_app.py
echo def unsafe_query(user_id): >> sample_project\vulnerable_app.py
echo     # SQL Injection vulnerability >> sample_project\vulnerable_app.py
echo     query = f"SELECT * FROM users WHERE id = {user_id}" >> sample_project\vulnerable_app.py
echo     return query >> sample_project\vulnerable_app.py

echo ✅ Sample project created

echo.
echo 🎉 Installation completed successfully!
echo.
echo Quick Start:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Run CLI audit: python code_auditor.py --directory sample_project
echo 3. Launch dashboard: streamlit run app.py
echo 4. Open browser: http://localhost:8501
echo.
echo For Docker users:
echo 1. docker-compose up -d
echo 2. Open browser: http://localhost:8501
echo.
echo Documentation: README.md
pause