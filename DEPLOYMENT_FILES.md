# Deployment Files Reference

## 📁 File Structure for Render Deployment

```
scrapergov/
├── api.py                      # Main FastAPI application ⭐
├── icare_address_search.py     # Scraping logic (core)
├── requirements.txt            # Python dependencies ⭐
├── render.yaml                 # Render config (automatic) ⭐
├── Procfile                    # Alternative config ⭐
├── .gitignore                  # Git ignore rules ⭐
│
├── README.md                   # Main documentation
├── DEPLOY_NOW.md              # Quick deployment guide 🚀
├── RENDER_DEPLOYMENT.md       # Detailed deployment guide 📖
├── DEPLOYMENT_SUMMARY.md      # This summary
├── DEPLOYMENT_FILES.md        # File reference (this file)
│
├── WINDOWS_SETUP_GUIDE.md     # Windows local setup
├── QUICK_START.md             # Quick local setup
├── HANDOFF_CHECKLIST.md       # Handoff guide
│
├── test_api.py                # API tests
└── start_server.bat           # Windows startup script
```

**Files marked with ⭐ are required for Render deployment**

---

## 🔧 Required Deployment Files

### 1. `api.py`
**Purpose:** Main application file
**Contains:**
- FastAPI app definition
- API endpoints
- Request/response models
- CORS configuration

**Required by:** Render to run your application

---

### 2. `requirements.txt`
**Purpose:** Lists Python dependencies
**Contains:**
```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
requests>=2.31.0
beautifulsoup4>=4.12.3
pydantic>=2.5.3
gunicorn>=21.2.0
```

**Required by:** Render to install dependencies during build

---

### 3. `render.yaml`
**Purpose:** Deployment configuration
**Contains:**
- Service type (web)
- Runtime (Python)
- Build command
- Start command
- Environment variables

**Used by:** Render for automatic configuration

**Contents:**
```yaml
services:
  - type: web
    name: fairfax-property-api
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn api:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.12.0
```

---

### 4. `Procfile`
**Purpose:** Alternative deployment config
**Contains:**
```
web: uvicorn api:app --host 0.0.0.0 --port $PORT
```

**Used by:** Render if `render.yaml` is not present

**Note:** You can use either `render.yaml` OR `Procfile`, not both. `render.yaml` is more feature-rich.

---

### 5. `.gitignore`
**Purpose:** Tells Git which files to ignore
**Prevents:**
- Python cache files
- Virtual environments
- Environment variables
- IDE files
- OS files

**Important:** Keeps your repository clean

---

## 📚 Documentation Files

### Deployment Guides

| File | Purpose | When to Use |
|------|---------|-------------|
| `DEPLOY_NOW.md` | Quick 5-min guide | First time deploying |
| `RENDER_DEPLOYMENT.md` | Complete guide | Detailed steps needed |
| `DEPLOYMENT_SUMMARY.md` | Overview + reference | Understanding what was set up |
| `DEPLOYMENT_FILES.md` | File reference | Understanding file structure |

### Setup Guides

| File | Purpose | When to Use |
|------|---------|-------------|
| `README.md` | Main docs | API reference |
| `WINDOWS_SETUP_GUIDE.md` | Windows local setup | Setting up on Windows |
| `QUICK_START.md` | Quick local setup | Fast local testing |
| `HANDOFF_CHECKLIST.md` | Handoff info | Giving to another dev |

---

## 🎯 Which Files to Edit

### Frequently Modified:
- ✏️ `api.py` - Add/modify endpoints
- ✏️ `icare_address_search.py` - Update scraping logic
- ✏️ `requirements.txt` - Add new dependencies

### Rarely Modified:
- 🔒 `render.yaml` - Only if changing deployment config
- 🔒 `Procfile` - Only if not using render.yaml
- 🔒 `.gitignore` - Only if adding new file types to ignore

### Documentation (Update as Needed):
- 📝 `README.md` - Update API docs
- 📝 Other `.md` files - Update guides if process changes

---

## 📤 Files to Commit to Git

### Always Commit:
```
✅ api.py
✅ icare_address_search.py
✅ requirements.txt
✅ render.yaml
✅ Procfile
✅ .gitignore
✅ All .md documentation files
✅ test_api.py
```

### Never Commit:
```
❌ __pycache__/
❌ *.pyc
❌ .env (if created)
❌ venv/ or env/
❌ .DS_Store
❌ Personal notes
```

**Tip:** `.gitignore` handles this automatically!

---

## 🔄 Deployment File Flow

```
1. Developer edits code
   ├── api.py
   └── requirements.txt (if new deps)

2. Commit & Push to GitHub
   └── git push

3. Render detects changes
   └── Reads render.yaml or Procfile

4. Render builds
   └── Runs: pip install -r requirements.txt

5. Render starts
   └── Runs: uvicorn api:app --host 0.0.0.0 --port $PORT

6. API is live! 🎉
```

---

## 🛠️ Configuration Comparison

### Using `render.yaml` (Recommended):

**Pros:**
- ✅ More configuration options
- ✅ Can specify environment variables
- ✅ Can set Python version
- ✅ Better for complex setups
- ✅ Infrastructure as code

**Cons:**
- ⚠️ More verbose

### Using `Procfile`:

**Pros:**
- ✅ Simpler
- ✅ Less configuration
- ✅ Works across multiple platforms

**Cons:**
- ⚠️ Limited options
- ⚠️ Manual environment variable setup

**Recommendation:** Use `render.yaml` for better control

---

## 📋 Pre-Deployment Checklist

Before pushing to GitHub/Render:

### Code Files:
- [ ] `api.py` has all endpoints working
- [ ] `icare_address_search.py` has no errors
- [ ] All imports work correctly
- [ ] CORS is configured in `api.py`

### Config Files:
- [ ] `requirements.txt` lists all dependencies
- [ ] `render.yaml` or `Procfile` is present
- [ ] `.gitignore` is configured
- [ ] No sensitive data in code

### Testing:
- [ ] Local tests pass: `python test_api.py`
- [ ] Server starts locally: `uvicorn api:app --reload`
- [ ] All endpoints work in `/docs`

### Git:
- [ ] All files committed
- [ ] Pushed to GitHub
- [ ] Repository is accessible

---

## 🔍 File Dependencies

```
api.py
├── Imports from: icare_address_search.py
├── Uses: requests, fastapi, beautifulsoup4
└── Required by: uvicorn (to run)

requirements.txt
├── Lists all packages
└── Used by: pip install

render.yaml
├── Defines: build & start commands
└── Used by: Render platform

.gitignore
├── Prevents unwanted files
└── Used by: Git
```

---

## 💡 Quick Tips

### 1. Editing Files:
```bash
# Edit API code
nano api.py  # or use any text editor

# Add new dependency
echo "new-package>=1.0.0" >> requirements.txt

# Test locally first!
python -m uvicorn api:app --reload
```

### 2. Deploying Changes:
```bash
git add .
git commit -m "Description of changes"
git push
# Render auto-deploys! ✨
```

### 3. Checking Logs:
- Go to Render dashboard
- Click your service
- Click "Logs" tab

---

## 🎯 Essential Files Summary

| File | Required? | Purpose | Edit Frequency |
|------|-----------|---------|----------------|
| `api.py` | ✅ Yes | Main app | Often |
| `icare_address_search.py` | ✅ Yes | Core logic | Sometimes |
| `requirements.txt` | ✅ Yes | Dependencies | Sometimes |
| `render.yaml` | ✅ Yes* | Config | Rarely |
| `Procfile` | ⚠️ Alternative | Config | Rarely |
| `.gitignore` | ✅ Yes | Git rules | Rarely |
| Documentation | 📚 Helpful | Guides | As needed |

*Use either `render.yaml` OR `Procfile`, not both

---

## 🚀 Ready to Deploy?

You have all the files needed! Follow:
1. **[DEPLOY_NOW.md](DEPLOY_NOW.md)** for quick deployment
2. **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)** for detailed guide

---

**Questions about specific files?** Check the file itself - most have helpful comments!
