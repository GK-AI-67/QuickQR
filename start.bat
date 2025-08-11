@echo off
echo Starting QuickQR Application...
echo.

echo Starting Backend Server...
cd backend
start "Backend Server" cmd /k "python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Starting Frontend Server...
cd ..\frontend
start "Frontend Server" cmd /k "npm install && npm run dev"

echo.
echo QuickQR is starting up!
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:5173
echo.
echo Press any key to exit this window...
pause > nul 