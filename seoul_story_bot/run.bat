@echo off
chcp 65001 >nul
REM Run server accessible from other PCs (host 0.0.0.0)
uvicorn app.main:app --host 0.0.0.0 --port 8000
