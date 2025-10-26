# Fairfax County Property Search API

A FastAPI application for searching properties and retrieving tax information from Fairfax County iCare.

## 🎯 Live API

**Public API URL:** https://govtaxcheck.onrender.com

**📖 [Complete User Guide](USER_GUIDE.md)** - Learn how to use the API

**🔗 [Interactive Docs](https://govtaxcheck.onrender.com/docs)** - Try the API in your browser

---

## 🚀 Quick Deploy to Render (Free)

**Want to deploy this API to the cloud for free?**

👉 **[See DEPLOY_NOW.md](DEPLOY_NOW.md)** for 5-minute deployment guide

Your API will be live at: `https://YOUR-APP-NAME.onrender.com`

---

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   uvicorn api:app --reload --port 8001
   ```

3. **Access the API:**
   - API Base URL: `http://localhost:8001`
   - Interactive Swagger Docs: `http://localhost:8001/docs`
   - ReDoc Documentation: `http://localhost:8001/redoc`

## API Endpoints

### 1. Root Endpoint
- **GET** `/`
- Returns API information and available endpoints

```bash
curl http://localhost:8001/
```

### 2. Health Check
- **GET** `/health`
- Returns the health status of the API

```bash
curl http://localhost:8001/health
```

### 3. Search Address
- **POST** `/search/address`
- Search for properties by address in Fairfax County

**Request Body:**
```json
{
  "number": "100",      // Street number (optional)
  "street": "MAIN",     // Street name (required)
  "suffix": "ST",       // Street suffix (optional)
  "unit": "",           // Unit/Apt number (optional)
  "page_size": "15"     // Results per page (optional, default: 15)
}
```

**Example:**
```bash
curl -X POST "http://localhost:8001/search/address" \
  -H "Content-Type: application/json" \
  -d '{"street": "MAIN", "suffix": "ST"}'
```

**Response:**
```json
{
  "success": true,
  "count": 15,
  "results": [
    {
      "Map #": "0583 01  0001",
      "Owner": "SCHOOL BOARD OF FAIRFAX COUNTY",
      "Property Address": "9515 MAIN ST",
      "Last Sale": "N/A",
      "DetailURL": "https://icare.fairfaxcounty.gov/ffxcare/Datalets/Datalet.aspx?sIndex=0&idx=1"
    },
    ...
  ]
}
```

### 4. Get Tax Summary
- **GET** `/tax-summary`
- Get tax summary for a specific property

**Query Parameters:**
- `detail_url` (required): The DetailURL obtained from the address search results

**Example:**
```bash
curl -X GET "http://localhost:8001/tax-summary?detail_url=https://icare.fairfaxcounty.gov/ffxcare/Datalets/Datalet.aspx?sIndex=0&idx=1"
```

**Response:**
```json
{
  "success": true,
  "title": "Tax Summary",
  "stub_number": "123456",
  "periods": [
    {
      "year": "2024",
      "label": "Current",
      "amount_paid": "$5,000.00",
      "balance_due": "$0.00",
      "amount_paid_decimal": 5000.0,
      "balance_due_decimal": 0.0
    }
  ],
  "total": {
    "year": "Total",
    "label": "",
    "amount_paid": "$5,000.00",
    "balance_due": "$0.00",
    "amount_paid_decimal": 5000.0,
    "balance_due_decimal": 0.0
  },
  "tax_year_code": "2024"
}
```

## Testing Results

The API has been successfully tested with the following results:

✅ **Address Search Endpoint** - Working perfectly
- Successfully searches Fairfax County properties
- Returns property details including address, owner, map number, and detail URLs
- Tested with: "MAIN ST" search returned 15 results

✅ **Health Check Endpoint** - Working
- Returns `{"status": "healthy"}`

✅ **Root Endpoint** - Working
- Returns API information and endpoint list

⚠️ **Tax Summary Endpoint** - Functional but limited
- The endpoint works correctly
- Some properties may not have tax information available (commercial/government properties)
- Returns appropriate error messages when tax data is not found

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Missing required parameters (e.g., street name)
- **422 Unprocessable Entity**: Unable to parse tax details from the page
- **500 Internal Server Error**: Request failures or unexpected errors

## Response Models

All responses are properly typed using Pydantic models for validation and documentation.

## Interactive Documentation

Visit `http://localhost:8001/docs` for interactive API documentation where you can:
- View all endpoints and their parameters
- Test API calls directly from the browser
- See request/response schemas
- View example requests and responses

## Original CLI Tool

The original CLI tool is still available in [icare_address_search.py](icare_address_search.py). Run it with:

```bash
python icare_address_search.py
```
