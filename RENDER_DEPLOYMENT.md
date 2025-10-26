# Deploy to Render - Step by Step Guide

This guide will walk you through deploying the Fairfax County Property Search API to Render for free.

## What is Render?

Render is a cloud platform that lets you deploy web applications for free. Your API will be accessible from anywhere on the internet at a URL like: `https://your-app-name.onrender.com`

## Prerequisites

1. A GitHub account (free) - [Sign up here](https://github.com/signup)
2. A Render account (free) - [Sign up here](https://render.com/signup)
3. Your project code

---

## Step 1: Push Code to GitHub

### Option A: Using GitHub Desktop (Easiest for Windows)

1. **Download GitHub Desktop:**
   - Go to: https://desktop.github.com/
   - Download and install

2. **Create a new repository:**
   - Open GitHub Desktop
   - Click "File" → "New Repository"
   - Name: `fairfax-property-api`
   - Local Path: Choose your project folder
   - Click "Create Repository"

3. **Add your files:**
   - GitHub Desktop will show all your project files
   - Add a commit message: "Initial commit - Property Search API"
   - Click "Commit to main"

4. **Publish to GitHub:**
   - Click "Publish repository"
   - Uncheck "Keep this code private" (or leave it checked if you prefer)
   - Click "Publish Repository"

### Option B: Using Git Command Line

```bash
# Navigate to your project folder
cd path/to/scrapergov

# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit - Property Search API"

# Create repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/fairfax-property-api.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy to Render

### A. Sign in to Render

1. Go to: https://render.com/
2. Click "Sign In" (or "Get Started")
3. Sign in with GitHub

### B. Create New Web Service

1. **Click "New +" button** (top right)
2. Select **"Web Service"**

### C. Connect Your Repository

1. **Connect GitHub account** if not already connected
2. **Find your repository:** `fairfax-property-api`
3. Click **"Connect"**

### D. Configure the Service

Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `fairfax-property-api` (or any name you like) |
| **Region** | Choose closest to you (e.g., Oregon USA) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn api:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | **Free** |

### E. Advanced Settings (Optional)

Click "Advanced" and add:

**Environment Variables:**
- Key: `PYTHON_VERSION`
- Value: `3.12.0`

### F. Deploy

1. Click **"Create Web Service"** at the bottom
2. Wait for deployment (5-10 minutes first time)
3. Watch the logs to see progress

---

## Step 3: Test Your Deployed API

Once deployment completes, you'll get a URL like:
```
https://fairfax-property-api.onrender.com
```

### Test Endpoints:

1. **Health Check:**
   ```
   https://fairfax-property-api.onrender.com/health
   ```

2. **Interactive Docs:**
   ```
   https://fairfax-property-api.onrender.com/docs
   ```

3. **Search Example (PowerShell):**
   ```powershell
   Invoke-RestMethod -Method Post `
     -Uri "https://fairfax-property-api.onrender.com/search/address" `
     -ContentType "application/json" `
     -Body '{"street":"MAIN","suffix":"ST"}'
   ```

4. **Search Example (curl):**
   ```bash
   curl -X POST "https://fairfax-property-api.onrender.com/search/address" \
     -H "Content-Type: application/json" \
     -d '{"street":"MAIN","suffix":"ST"}'
   ```

---

## Step 4: Get Your API URL

After deployment:

1. Go to your Render dashboard
2. Click on your service
3. Copy the URL at the top (e.g., `https://fairfax-property-api.onrender.com`)
4. Share this URL with anyone who needs to use your API!

---

## Important Notes About Free Tier

### ⚠️ Free Tier Limitations:

1. **Service Spins Down:**
   - After 15 minutes of inactivity, the service sleeps
   - First request after sleep takes ~50 seconds to wake up
   - Subsequent requests are fast

2. **Solution for Slow Wake-up:**
   - Use a service like [UptimeRobot](https://uptimerobot.com/) (free) to ping your API every 14 minutes
   - Or upgrade to paid tier ($7/month) for always-on service

3. **Other Limitations:**
   - 750 hours/month of runtime (enough for most uses)
   - Services spin down after 15 min inactivity
   - Custom domains require paid plan

---

## Updating Your Deployed API

When you make changes to your code:

### Using GitHub Desktop:
1. Make your code changes
2. Open GitHub Desktop
3. Write a commit message
4. Click "Commit to main"
5. Click "Push origin"
6. Render will automatically redeploy!

### Using Git Command Line:
```bash
git add .
git commit -m "Description of changes"
git push
```

Render will automatically detect the changes and redeploy.

---

## Troubleshooting

### Build Failed
**Check the logs:**
1. Go to Render dashboard
2. Click on your service
3. Click "Logs" tab
4. Look for error messages

**Common issues:**
- Missing dependencies: Update `requirements.txt`
- Wrong Python version: Set `PYTHON_VERSION` environment variable
- Syntax errors: Test locally first

### Service Won't Start
**Check start command:**
- Should be: `uvicorn api:app --host 0.0.0.0 --port $PORT`
- Make sure `$PORT` is in caps

**Check environment:**
- Python version set to 3.12.0
- All required packages in requirements.txt

### API Returns Errors
**Check the logs:**
1. Go to service in Render
2. Click "Logs"
3. Look for Python errors

**Test locally first:**
```bash
python -m uvicorn api:app --reload --port 8001
```

If it works locally but not on Render, check environment variables.

---

## Monitoring Your API

### View Logs
1. Go to Render dashboard
2. Click your service
3. Click "Logs" tab
4. See real-time logs of API requests

### Metrics (Free Tier)
- Request count
- Response times
- Error rates
- Memory usage

### Set Up Alerts
1. Go to service settings
2. Add notification email
3. Get alerts for:
   - Deploy failures
   - Service crashes
   - High error rates

---

## Custom Domain (Optional - Paid Feature)

To use your own domain (e.g., `api.yourdomain.com`):

1. **Upgrade to Paid Plan** ($7/month)
2. **Add Custom Domain:**
   - Go to service settings
   - Click "Custom Domains"
   - Add your domain
3. **Update DNS:**
   - Add CNAME record pointing to Render
   - Follow Render's instructions

---

## Environment Variables (If Needed Later)

To add secrets or configuration:

1. Go to service in Render
2. Click "Environment"
3. Add variables:
   - Key: `YOUR_KEY_NAME`
   - Value: `your_secret_value`
4. Click "Save Changes"
5. Service will redeploy automatically

---

## Security Best Practices

1. **Rate Limiting (Future Enhancement):**
   ```python
   # Add to api.py
   from slowapi import Limiter
   from slowapi.util import get_remote_address

   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   ```

2. **CORS Configuration (If needed for web apps):**
   ```python
   from fastapi.middleware.cors import CORSMiddleware

   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Update with your domains
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. **API Keys (Future Enhancement):**
   - Add authentication
   - Require API keys for requests
   - Track usage per user

---

## Cost Breakdown

### Free Tier (Current):
- ✅ 750 hours/month
- ✅ Unlimited deploys
- ✅ Automatic HTTPS
- ✅ Free subdomain
- ⚠️ Spins down after 15 min
- ⚠️ 512 MB RAM

### Paid Tier ($7/month):
- ✅ Always on (no spin down)
- ✅ Custom domain
- ✅ 512 MB RAM (more available)
- ✅ Priority support
- ✅ Better performance

---

## Quick Reference Commands

### Local Testing:
```bash
# Start server locally
uvicorn api:app --reload --port 8001

# Run tests
python test_api.py
```

### Git Commands:
```bash
# Check status
git status

# Add and commit
git add .
git commit -m "Your message"

# Push to GitHub (triggers Render deploy)
git push
```

### API Testing:
```bash
# Health check
curl https://your-app.onrender.com/health

# Search
curl -X POST "https://your-app.onrender.com/search/address" \
  -H "Content-Type: application/json" \
  -d '{"street":"MAIN","suffix":"ST"}'
```

---

## Next Steps After Deployment

1. ✅ Test all endpoints using `/docs`
2. ✅ Set up UptimeRobot to keep service warm (optional)
3. ✅ Share API URL with users
4. ✅ Monitor logs for errors
5. ✅ Consider upgrading if you need always-on service

---

## Getting Help

### Render Support:
- Documentation: https://render.com/docs
- Community: https://community.render.com/
- Status: https://status.render.com/

### API Issues:
- Check logs in Render dashboard
- Test locally first
- Review error messages

---

## Summary Checklist

Before going live, verify:

- [ ] Code pushed to GitHub
- [ ] Render service created and deployed
- [ ] Build completed successfully
- [ ] Service is running
- [ ] `/health` endpoint returns "healthy"
- [ ] `/docs` page loads
- [ ] `/search/address` endpoint works
- [ ] API URL saved and shared
- [ ] Monitoring set up (optional)
- [ ] UptimeRobot configured (optional)

---

**Congratulations!** Your API is now live and accessible from anywhere! 🎉

Your API URL: `https://YOUR-APP-NAME.onrender.com`

Share this URL with anyone who needs to access the Fairfax County Property Search API.
