@echo off
echo ========================================
echo    QuickQR - Mobile Access Setup
echo ========================================
echo.

echo Starting Backend Server...
cd backend
call venv\Scripts\activate.bat
start "QuickQR Backend" cmd /k "python main.py"
cd ..

echo.
echo Starting Frontend Server...
cd frontend
start "QuickQR Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ========================================
echo    Application URLs for Mobile Access
echo ========================================
echo.
echo Frontend: http://192.168.2.120:5174/
echo Backend:  http://192.168.2.120:8000/
echo API Docs: http://192.168.2.120:8000/docs
echo.
echo ========================================
echo    Instructions for Mobile Access
echo ========================================
echo 1. Make sure your mobile device is on the same WiFi network
echo 2. Open browser on mobile and go to: http://192.168.2.120:5174/
echo 3. Generate QR codes and scan them with your mobile device
echo.
echo Press any key to exit...
pause >nul 