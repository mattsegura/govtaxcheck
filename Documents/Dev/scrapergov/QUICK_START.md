# Quick Start Guide - Windows

## TL;DR - Get Running in 5 Minutes

### 1. Install Python (5 minutes)
1. Download: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Run installer
3. ✅ **CHECK THE BOX: "Add Python to PATH"**
4. Click "Install Now"

### 2. Setup API (2 minutes)
Open Command Prompt in the project folder:
```cmd
pip install -r requirements.txt
python -m uvicorn api:app --reload --port 8001
```

### 3. Test It
Open browser: [http://localhost:8001/docs](http://localhost:8001/docs)

---

## Basic Commands

### Start Server
```cmd
python -m uvicorn api:app --reload --port 8001
```

### Stop Server
Press `Ctrl + C` in the Command Prompt window

---

## Testing the API

### Open Interactive Docs
Browser: [http://localhost:8001/docs](http://localhost:8001/docs)

### Search Example (PowerShell)
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8001/search/address" `
  -ContentType "application/json" `
  -Body '{"street":"MAIN","suffix":"ST"}'
```

### Search Example (curl)
```cmd
curl -X POST "http://localhost:8001/search/address" -H "Content-Type: application/json" -d "{\"street\":\"MAIN\",\"suffix\":\"ST\"}"
```

---

## File Checklist

Make sure you have these files:
- ✅ `api.py` - Main API application
- ✅ `icare_address_search.py` - Core scraping logic
- ✅ `requirements.txt` - Dependencies
- ✅ `README.md` - Full documentation
- ✅ `WINDOWS_SETUP_GUIDE.md` - Detailed Windows instructions
- ✅ `QUICK_START.md` - This file

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "python is not recognized" | Reinstall Python with "Add to PATH" checked |
| "pip is not recognized" | Use `python -m pip` instead of `pip` |
| Port 8001 in use | Change port: `--port 8002` |
| Dependencies won't install | Update pip: `python -m pip install --upgrade pip` |

---

## Need Help?
See [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md) for detailed instructions.
