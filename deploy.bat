@echo off
echo ========================================
echo    QuickQR - Internet Deployment
echo ========================================
echo.

echo Step 1: Initialize Git Repository
git init
git add .
git commit -m "Initial commit for deployment"
echo.

echo Step 2: Create GitHub Repository
echo Please create a new repository on GitHub:
echo 1. Go to https://github.com/new
echo 2. Name it: quickqr
echo 3. Make it public
echo 4. Don't initialize with README
echo.

echo Step 3: Connect to GitHub
set /p GITHUB_USERNAME="Enter your GitHub username: "
git remote add origin https://github.com/%GITHUB_USERNAME%/quickqr.git
git branch -M main
git push -u origin main
echo.

echo Step 4: Deploy Backend to Railway
echo 1. Go to https://railway.app
echo 2. Sign up with GitHub
echo 3. Click "New Project" -> "Deploy from GitHub repo"
echo 4. Select your quickqr repository
echo 5. Set root directory to: backend
echo 6. Deploy!
echo.

echo Step 5: Deploy Frontend to Vercel
echo 1. Go to https://vercel.com
echo 2. Sign up with GitHub
echo 3. Click "New Project"
echo 4. Import your quickqr repository
echo 5. Set root directory to: frontend
echo 6. Deploy!
echo.

echo ========================================
echo    Deployment URLs
echo ========================================
echo.
echo After deployment, you'll get URLs like:
echo Backend:  https://quickqr-backend-production.up.railway.app
echo Frontend: https://quickqr-frontend.vercel.app
echo.
echo Update the CORS settings in backend/app/core/config.py
echo with your frontend URL!
echo.
echo Press any key to exit...
pause >nul 