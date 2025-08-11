# 🚀 Render Deployment - Quick Setup

## 📋 Current Status
✅ Logged into Render
⏳ Ready to deploy backend and frontend

## 🔧 Next Steps

### 1. Deploy Backend
1. Click "New +" → "Web Service"
2. Connect GitHub repository
3. Configure:
   - **Name:** `quickqr-backend`
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 2. Deploy Frontend
1. Click "New +" → "Static Site"
2. Connect same GitHub repository
3. Configure:
   - **Name:** `quickqr-frontend`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`

### 3. Get Your URLs
After deployment, you'll get:
- Backend: `https://your-backend-name.onrender.com`
- Frontend: `https://your-frontend-name.onrender.com`

### 4. Update Configuration
Once you have the URLs, we'll update:
- Frontend API configuration
- Backend CORS settings

## 🎯 Expected Result
Your QuickQR app will be live on the internet and accessible from anywhere!

## 📱 Test
Generate a QR code and scan it with your mobile device - it should work perfectly! 