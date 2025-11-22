# 🚀 Deployment Guide - Tourism Guide System

## Best Platforms for Your Project

I recommend these platforms based on your project structure:

### 🏆 **Recommended Options**

1. **Render.com** ⭐ BEST OVERALL
   - ✅ Free tier available
   - ✅ Easy deployment
   - ✅ Supports both backend and frontend
   - ✅ Auto-deploy from GitHub
   - ✅ Great for beginners

2. **Railway.app** ⭐ DEVELOPER FRIENDLY
   - ✅ Free $5 credit/month
   - ✅ One-click deploy
   - ✅ Great dashboard
   - ✅ Easy environment variables

3. **Vercel** (Frontend) + **Railway/Render** (Backend)
   - ✅ Best performance
   - ✅ Free tiers
   - ✅ Global CDN for frontend
   - ✅ Split deployment

---

## 📋 Deployment Checklist

### ✅ What You Have
- [x] FastAPI backend
- [x] Single HTML frontend
- [x] Requirements.txt
- [x] Docker support
- [x] Environment config
- [x] No database (good for deployment!)

### ⚠️ What You Need
- [ ] GitHub repository (recommended)
- [ ] Environment variables setup
- [ ] Production configuration
- [ ] CORS configuration for production

---

## 🎯 Option 1: Render.com (Recommended)

### Why Render?
- ✅ Easiest to use
- ✅ Free tier (750 hours/month)
- ✅ Auto-deploy from Git
- ✅ Built-in SSL
- ✅ Static site + Web service

### Steps:

#### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

#### 2. Deploy Backend on Render
- Go to: https://render.com
- Click "New +" → "Web Service"
- Connect your GitHub repo
- Settings:
  - **Name:** tourism-guide-backend
  - **Environment:** Python 3
  - **Build Command:** `pip install -r backend/requirements.txt`
  - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  - **Plan:** Free

#### 3. Deploy Frontend on Render
- Click "New +" → "Static Site"
- Connect same GitHub repo
- Settings:
  - **Name:** tourism-guide-frontend
  - **Build Command:** (leave empty)
  - **Publish Directory:** `frontend`
  - **Plan:** Free

#### 4. Update Frontend API URL
Update `frontend/index.html`:
```javascript
const API_URL = 'https://tourism-guide-backend.onrender.com';
```

---

## 🎯 Option 2: Railway.app

### Why Railway?
- ✅ $5 free credit/month
- ✅ Beautiful UI
- ✅ One command deploy
- ✅ Great for full-stack

### Steps:

#### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

#### 2. Login & Deploy
```bash
railway login
cd backend
railway init
railway up
```

#### 3. Set Environment Variables
```bash
railway variables set ENVIRONMENT=production
```

#### 4. Deploy Frontend on Vercel
```bash
cd frontend
npx vercel
```

---

## 🎯 Option 3: Vercel (Frontend) + Render (Backend)

### Why Split?
- ✅ Best performance
- ✅ Vercel excellent for static sites
- ✅ Global CDN
- ✅ Both have free tiers

### Frontend on Vercel:
```bash
cd frontend
npm install -g vercel
vercel
```

### Backend on Render:
(Same as Option 1)

---

## 📝 Pre-Deployment Setup

Let me create the necessary files for you...

---

## 🔐 Environment Variables Needed

For production, set these:
```
ENVIRONMENT=production
PORT=8000
ALLOWED_ORIGINS=https://your-frontend-url.com
```

---

## 🎨 Files I'll Create

1. `render.yaml` - Render configuration
2. `railway.json` - Railway configuration  
3. `vercel.json` - Vercel configuration
4. `Procfile` - For various platforms
5. `.env.example` - Example environment file
6. `DEPLOYMENT.md` - Detailed deployment guide

---

## 💰 Cost Comparison

| Platform | Backend | Frontend | Total/Month |
|----------|---------|----------|-------------|
| **Render** | Free (750hrs) | Free | $0 |
| **Railway** | $5 credit | - | ~$0-5 |
| **Vercel + Render** | Free | Free | $0 |
| **Heroku** | $0 (limited) | $0 | $0 |

**Recommendation:** Start with Render (completely free!)

---

## 🚀 Quick Start - Render Deployment

I'll create all necessary files now. Then you can:

1. Push to GitHub
2. Connect to Render
3. Deploy in 5 minutes!

Let me create the deployment files...
