@echo off
echo Starting QuickQR Application...
echo.

echo Starting Backend Server...
cd backend
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
start "Backend Server" cmd /k "call venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Starting Frontend Server...
cd ..\frontend
REM Ensure all required dependencies for TSX/React/TypeScript
npm install react react-dom @types/react @types/react-dom framer-motion react-hot-toast lucide-react --save
npm install
start "Frontend Server" cmd /k "npm run dev"

echo.
echo QuickQR is starting up!
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:5173
echo.
echo Press any key to exit this window...
pause > nul