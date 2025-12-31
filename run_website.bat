@echo off
TITLE Intelligent README Generator
echo ==========================================
echo Starting Intelligent README Generator...
echo ==========================================

cd /d "%~dp0"

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH!
    echo Please install Python 3.11+ and add it to your PATH.
    pause
    exit /b
)

:: Validate imports / dependencies (optional but helpful check)
echo Verifying core dependencies...
python -c "import streamlit, tree_sitter, networkx" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Some dependencies seem to be missing.
    echo Attempting to install from pyproject.toml / requirements...
    pip install .
)

echo.
echo Launching Streamlit App...
echo Press Ctrl+C to stop the server.
echo.

python -m streamlit run src/web.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The application crashed or was stopped.
    pause
)
