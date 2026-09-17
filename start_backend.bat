@echo off
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8010 ^| findstr LISTENING') do taskkill /PID %%a /F >nul 2>&1
cd /d C:\Users\ASUS\Desktop\ProjectPilot-AI\backend
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --host 127.0.0.1 --port 8010
pause