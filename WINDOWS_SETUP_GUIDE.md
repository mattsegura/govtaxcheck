# Windows Setup Guide - Fairfax County Property Search API

Complete guide for setting up and running the Property Search API on Windows.

## Prerequisites Installation

### Step 1: Install Python

1. **Download Python:**
   - Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Download Python 3.11 or 3.12 (recommended)
   - Click on "Download Python 3.12.x"

2. **Install Python:**
   - Run the downloaded installer
   - ⚠️ **IMPORTANT**: Check the box "Add Python to PATH" at the bottom of the installer
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close" when done

3. **Verify Installation:**
   - Open Command Prompt (press `Win + R`, type `cmd`, press Enter)
   - Type the following command and press Enter:
     ```cmd
     python --version
     ```
   - You should see something like: `Python 3.12.x`
   - Also verify pip is installed:
     ```cmd
     pip --version
     ```

### Step 2: Download the Project Files

1. **Get the Project Files:**
   - Download all files from the project folder
   - Make sure you have these files:
     - `api.py`
     - `icare_address_search.py`
     - `requirements.txt`
     - `README.md`
     - `WINDOWS_SETUP_GUIDE.md`

2. **Create a Project Folder:**
   - Create a new folder on your computer (e.g., `C:\PropertySearchAPI`)
   - Copy all the project files into this folder

## Setting Up the API

### Step 1: Open Command Prompt in Project Folder

1. **Navigate to Your Project Folder:**
   - Open File Explorer
   - Navigate to your project folder (e.g., `C:\PropertySearchAPI`)
   - Click in the address bar at the top
   - Type `cmd` and press Enter
   - A Command Prompt window will open in that folder

### Step 2: Install Dependencies

In the Command Prompt window, run:

```cmd
pip install -r requirements.txt
```

This will install all necessary packages:
- FastAPI (web framework)
- Uvicorn (web server)
- Requests (HTTP library)
- BeautifulSoup4 (HTML parser)
- Pydantic (data validation)

**Note:** You may see some warning messages - this is normal as long as the installation completes successfully.

### Step 3: Run the API Server

In the same Command Prompt window, run:

```cmd
python -m uvicorn api:app --reload --port 8001
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**The API is now running!** 🎉

## Using the API

### Option 1: Interactive Documentation (Easiest)

1. Open your web browser (Chrome, Edge, Firefox, etc.)
2. Go to: [http://localhost:8001/docs](http://localhost:8001/docs)
3. You'll see an interactive interface where you can test the API

**To test the search:**
1. Click on "POST /search/address"
2. Click "Try it out"
3. Edit the request body (example):
   ```json
   {
     "street": "MAIN",
     "suffix": "ST",
     "number": "",
     "unit": "",
     "page_size": "15"
   }
   ```
4. Click "Execute"
5. Scroll down to see the results

### Option 2: Using PowerShell

Open PowerShell (press `Win + X`, select "Windows PowerShell"):

**Search for an address:**
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8001/search/address" `
  -ContentType "application/json" `
  -Body '{"street":"MAIN","suffix":"ST"}' | ConvertTo-Json
```

**Check health:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8001/health"
```

### Option 3: Using Command Prompt with curl

Modern Windows 10/11 has curl built-in:

**Search for an address:**
```cmd
curl -X POST "http://localhost:8001/search/address" -H "Content-Type: application/json" -d "{\"street\":\"MAIN\",\"suffix\":\"ST\"}"
```

**Check health:**
```cmd
curl http://localhost:8001/health
```

## API Endpoints

### 1. Search for Properties
- **Endpoint:** `POST /search/address`
- **Purpose:** Find properties in Fairfax County
- **Required:** `street` (street name)
- **Optional:** `number`, `suffix`, `unit`, `page_size`

### 2. Get Tax Summary
- **Endpoint:** `GET /tax-summary`
- **Purpose:** Get tax details for a specific property
- **Required:** `detail_url` (from search results)

### 3. Health Check
- **Endpoint:** `GET /health`
- **Purpose:** Verify API is running

### 4. API Info
- **Endpoint:** `GET /`
- **Purpose:** Get API information and available endpoints

## Stopping the Server

To stop the API server:
1. Go to the Command Prompt window where the server is running
2. Press `Ctrl + C`
3. Confirm if prompted

## Troubleshooting

### Problem: "python is not recognized"
**Solution:**
- Python wasn't added to PATH during installation
- Uninstall Python
- Reinstall and make sure to check "Add Python to PATH"

### Problem: "pip is not recognized"
**Solution:**
- Try using `python -m pip` instead of `pip`
- Example: `python -m pip install -r requirements.txt`

### Problem: "Port 8001 is already in use"
**Solution:**
- Change the port number in the run command:
  ```cmd
  python -m uvicorn api:app --reload --port 8002
  ```
- Then access the API at `http://localhost:8002`

### Problem: Dependencies fail to install
**Solution:**
- Update pip first:
  ```cmd
  python -m pip install --upgrade pip
  ```
- Then try installing requirements again

### Problem: "No module named 'uvicorn'"
**Solution:**
- The dependencies weren't installed properly
- Run the installation command again:
  ```cmd
  pip install -r requirements.txt
  ```

## Running as a Background Service

If you want to run the API continuously:

1. **Create a batch file** (`start_api.bat`):
   ```batch
   @echo off
   cd C:\PropertySearchAPI
   python -m uvicorn api:app --port 8001
   pause
   ```

2. **Double-click the batch file** to start the server

3. **Create a shortcut** and place it in your Startup folder to run on Windows startup:
   - Press `Win + R`
   - Type: `shell:startup`
   - Press Enter
   - Create a shortcut to your batch file in this folder

## Network Access (Optional)

To allow other computers on your network to access the API:

1. **Run with host parameter:**
   ```cmd
   python -m uvicorn api:app --host 0.0.0.0 --port 8001
   ```

2. **Configure Windows Firewall:**
   - Go to Windows Defender Firewall
   - Click "Advanced settings"
   - Click "Inbound Rules" → "New Rule"
   - Select "Port" → Next
   - Select "TCP" → Enter port 8001 → Next
   - Allow the connection → Next
   - Apply to all profiles → Next
   - Give it a name (e.g., "Property Search API") → Finish

3. **Find your computer's IP address:**
   ```cmd
   ipconfig
   ```
   - Look for "IPv4 Address" under your network adapter

4. **Access from other computers:**
   - Use: `http://YOUR_IP_ADDRESS:8001`

## Example Use Cases

### Search for a specific address:
```json
{
  "number": "4000",
  "street": "LEGATO",
  "suffix": "RD"
}
```

### Search all properties on a street:
```json
{
  "street": "MAIN",
  "suffix": "ST"
}
```

### Search with apartment/unit:
```json
{
  "number": "100",
  "street": "MAIN",
  "suffix": "ST",
  "unit": "APT 5"
}
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all files are in the correct folder
3. Make sure Python and all dependencies are properly installed
4. Check that no other application is using port 8001

## Additional Resources

- **Python Documentation:** [https://docs.python.org/3/](https://docs.python.org/3/)
- **FastAPI Documentation:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **Interactive API Docs:** [http://localhost:8001/docs](http://localhost:8001/docs) (when server is running)
