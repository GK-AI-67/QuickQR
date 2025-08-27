@echo off
REM Install requirements
C:\Users\ADMIN\anaconda3\python.exe -m pip install -r requirements.txt
REM Start FastAPI with Uvicorn
C:\Users\ADMIN\anaconda3\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
