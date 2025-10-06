# 🚀 Dashboard Deployment Guide

## 📋 Pre-deployment Setup

First, create a production build of your React dashboard:

```bash
cd /Users/praveen/Downloads/CanadianMedicalDevices/dashboard
npm run build
```

This creates an optimized `build/` folder ready for deployment.

---

## 🌟 **Option 1: Vercel (Recommended - FREE)**

### **Why Vercel?**
- ✅ Free for personal projects
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Easy React deployment
- ✅ Custom domain support

### **Steps:**
```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Navigate to dashboard folder
cd /Users/praveen/Downloads/CanadianMedicalDevices/dashboard

# 3. Deploy (first time setup)
vercel

# 4. Follow prompts:
# - Login with GitHub/Google
# - Project name: medical-device-dashboard
# - Framework: Create React App (auto-detected)
# - Build command: npm run build (default)
# - Output directory: build (default)
```

### **Result:**
- Live URL: `https://medical-device-dashboard-abc123.vercel.app`
- Auto-deploys on Git push (if connected to GitHub)

---

## 🌐 **Option 2: Netlify (FREE)**

### **Manual Upload:**
1. Run `npm run build`
2. Go to [netlify.com](https://netlify.com)
3. Drag & drop the `build/` folder
4. Get instant URL: `https://amazing-name-123456.netlify.app`

### **CLI Deployment:**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build and deploy
cd /Users/praveen/Downloads/CanadianMedicalDevices/dashboard
npm run build
netlify deploy --prod --dir=build
```

---

## 🐙 **Option 3: GitHub Pages (FREE)**

### **Setup:**
```bash
# 1. Install gh-pages
cd /Users/praveen/Downloads/CanadianMedicalDevices/dashboard
npm install --save-dev gh-pages

# 2. Add to package.json (add this line to scripts):
"predeploy": "npm run build",
"deploy": "gh-pages -d build"

# 3. Add homepage URL (add this to package.json):
"homepage": "https://yourusername.github.io/medical-device-dashboard"

# 4. Deploy
npm run deploy
```

### **Requirements:**
- GitHub repository
- Enable GitHub Pages in repo settings

---

## ☁️ **Option 4: AWS S3 + CloudFront**

### **For Production/Enterprise:**
```bash
# 1. Build the app
npm run build

# 2. Upload to S3 bucket
aws s3 sync build/ s3://your-bucket-name --delete

# 3. Configure S3 for static website hosting
# 4. Optional: Add CloudFront CDN
```

### **Cost:** ~$1-5/month depending on traffic

---

## 🐳 **Option 5: Docker Deployment**

### **Create Dockerfile:**
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### **Deploy:**
```bash
# Build image
docker build -t medical-device-dashboard .

# Run locally
docker run -p 3000:80 medical-device-dashboard

# Deploy to cloud (AWS ECS, Google Cloud Run, etc.)
```

---

## 🎯 **Quick Start - Vercel (5 minutes)**

**Step 1:** Build the app
```bash
cd /Users/praveen/Downloads/CanadianMedicalDevices/dashboard
npm run build
```

**Step 2:** Install Vercel CLI
```bash
npm install -g vercel
```

**Step 3:** Deploy
```bash
vercel --prod
```

**Step 4:** Follow prompts and get your live URL!

---

## 🔧 **Environment Configuration**

### **For Production Deployment:**
Create `.env.production` in dashboard folder:
```bash
REACT_APP_API_URL=https://your-api-domain.com
REACT_APP_ENVIRONMENT=production
GENERATE_SOURCEMAP=false
```

### **Data Files Setup:**
Your dashboard uses JSON data files from `public/` folder:
- ✅ `comprehensive_dashboard_data.json` - Main data
- ✅ `reddit_evidence.json` - Reddit research
- ✅ `potential_legal_devices.json` - Legal analysis

These files will be included in the build automatically.

---

## 📊 **Performance Optimization**

### **Before Deployment:**
```bash
# 1. Optimize images in public/ folder
# 2. Enable gzip compression
# 3. Add service worker (optional)
# 4. Check bundle size
npm run build
npx serve -s build  # Test production build locally
```

---

## 🌍 **Custom Domain (Optional)**

### **After Deployment:**
1. **Vercel:** Project Settings → Domains → Add custom domain
2. **Netlify:** Site Settings → Domain Management → Add domain
3. **Configure DNS:** Point CNAME to deployment URL

---

## 🔒 **Security Considerations**

### **For Public Deployment:**
- ✅ Data is anonymized (no personal health info)
- ✅ All data from public Health Canada database
- ✅ Reddit data is public forum posts
- ✅ No API keys or sensitive data exposed

**Safe to deploy publicly!** 🛡️

---

## 🎉 **Recommended Quick Deployment**

**For immediate deployment, use Vercel:**

```bash
# One-time setup
npm install -g vercel

# Deploy (from dashboard folder)
cd /Users/praveen/Downloads/CanadianMedicalDevices/dashboard
vercel --prod

# Result: Live dashboard in ~2 minutes!
```

**You'll get:**
- 🌐 Live URL (e.g., `https://medical-device-dashboard.vercel.app`)
- 🔒 Automatic HTTPS
- ⚡ Global CDN
- 📱 Mobile responsive
- 🚀 Zero configuration

---

**Choose your deployment method and I can help you set it up!** 🚀