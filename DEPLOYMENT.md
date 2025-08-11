# 🚀 Quick Deployment Guide - Render

## **Step 1: Push to Git**
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - QuickQR with database"

# Add your GitHub repo
git remote add origin https://github.com/YOUR_USERNAME/QuickQR.git
git push -u origin main
```

## **Step 2: Deploy on Render**

### **Option A: Using render.yaml (Recommended)**
1. Go to [render.com](https://render.com)
2. Click "New +" → "Blueprint"
3. Connect your GitHub repo
4. Render will auto-detect `render.yaml`
5. Click "Apply" - it will create both web service and database

### **Option B: Manual Setup**
1. **Create Database:**
   - New + → PostgreSQL
   - Name: `quickqr-db`
   - Plan: Free

2. **Create Web Service:**
   - New + → Web Service
   - Connect GitHub repo
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && python main.py`
   - Add Environment Variable: `DATABASE_URL` (copy from PostgreSQL service)

## **Step 3: Environment Variables**
Add these in Render dashboard:
- `DATABASE_URL` (auto-added from PostgreSQL)
- `OPENAI_API_KEY` (your OpenAI key)
- `ENVIRONMENT=production`

## **Step 4: Deploy Frontend**
1. **Create Static Site:**
   - New + → Static Site
   - Connect GitHub repo
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`

2. **Add Environment Variable:**
   - `VITE_API_URL=https://your-backend-url.onrender.com/api/v1`

## **✅ Done!**
Your app will be live at:
- Frontend: `https://your-app-name.onrender.com`
- Backend: `https://your-backend-name.onrender.com`

## **Troubleshooting**
- Check Render logs for errors
- Ensure all environment variables are set
- Database connection issues? Check `DATABASE_URL` format 