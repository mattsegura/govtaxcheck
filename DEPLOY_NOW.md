# Deploy to Render in 5 Minutes ⚡

## Quick Deployment Steps

### 1️⃣ Push to GitHub (2 minutes)

**Option A - GitHub Desktop (Easiest):**
1. Download: https://desktop.github.com/
2. File → New Repository
3. Name: `fairfax-property-api`
4. Choose your project folder
5. Click "Publish repository"

**Option B - Command Line:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/fairfax-property-api.git
git push -u origin main
```

### 2️⃣ Deploy to Render (3 minutes)

1. Go to: https://render.com/
2. Sign in with GitHub
3. Click **"New +"** → **"Web Service"**
4. Select your repository: `fairfax-property-api`
5. Use these settings:

   | Setting | Value |
   |---------|-------|
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn api:app --host 0.0.0.0 --port $PORT` |
   | **Instance Type** | **Free** |

6. Click **"Create Web Service"**
7. Wait 5-10 minutes for first deploy

### 3️⃣ Get Your API URL

After deployment completes:
- Your URL: `https://YOUR-APP-NAME.onrender.com`
- Test it: `https://YOUR-APP-NAME.onrender.com/health`
- Docs: `https://YOUR-APP-NAME.onrender.com/docs`

---

## That's It! 🎉

Your API is now live and accessible from anywhere!

---

## Quick Test

```bash
# Replace YOUR-APP-NAME with your actual app name
curl https://YOUR-APP-NAME.onrender.com/health
```

Expected response:
```json
{"status": "healthy"}
```

---

## Important: Free Tier Note

⚠️ **Free tier sleeps after 15 minutes of inactivity**
- First request after sleep takes ~50 seconds
- Subsequent requests are fast

**Solution:** Use [UptimeRobot](https://uptimerobot.com/) (free) to ping every 14 minutes

---

## Update Your API

After making code changes:
```bash
git add .
git commit -m "Updated API"
git push
```

Render automatically redeploys! 🚀

---

## Need More Help?

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed instructions.

---

## Your Deployed Endpoints

Replace `YOUR-APP-NAME.onrender.com` with your actual URL:

- **Health:** `GET https://YOUR-APP-NAME.onrender.com/health`
- **Docs:** `GET https://YOUR-APP-NAME.onrender.com/docs`
- **Search:** `POST https://YOUR-APP-NAME.onrender.com/search/address`
- **Tax:** `GET https://YOUR-APP-NAME.onrender.com/tax-summary`

---

## Example API Call

```bash
curl -X POST "https://YOUR-APP-NAME.onrender.com/search/address" \
  -H "Content-Type: application/json" \
  -d '{"street":"MAIN","suffix":"ST"}'
```

---

**Questions?** Check [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for troubleshooting.
