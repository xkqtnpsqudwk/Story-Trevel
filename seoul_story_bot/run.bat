@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Seoul Story Routes

echo [1/3] Installing Python packages...
pip install -q -r requirements.txt
if errorlevel 1 (
  echo.
  echo ERROR: pip failed. Is Python/pip installed and on PATH?
  echo Try:  py -m pip install -r requirements.txt
  echo.
  pause
  exit /b 1
)

echo [2/3] Checking Ollama model...
where ollama >nul 2>nul && (ollama pull exaone3.5:2.4b) || (echo   Ollama not found - AI answers ^(F5^) OFF.  https://ollama.com)

echo [3/3] Starting server... Open http://localhost:8000   (Ctrl+C to stop)
uvicorn app.main:app --host 0.0.0.0 --port 8000

echo.
echo ============================================================
echo  Server stopped or failed to start. Read the message above.
echo  If "uvicorn is not recognized": run  python run.py  instead.
echo ============================================================
pause
