# User Guide - Fairfax County Property Search API

Complete guide for using the Fairfax County Property Search API to find property information and tax details.

**API Base URL:** https://govtaxcheck.onrender.com

**Interactive Documentation:** https://govtaxcheck.onrender.com/docs

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [API Endpoints](#api-endpoints)
3. [Search for Properties](#search-for-properties)
4. [Get Tax Summary](#get-tax-summary)
5. [Using the Interactive Docs](#using-the-interactive-docs)
6. [Code Examples](#code-examples)
7. [Common Use Cases](#common-use-cases)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Test the API (3 Steps)

**Step 1: Check API Status**
```
https://govtaxcheck.onrender.com/health
```
Should return: `{"status":"healthy"}`

**Step 2: Open Interactive Docs**
```
https://govtaxcheck.onrender.com/docs
```

**Step 3: Try a Search**
Search for properties on "MAIN ST":
```json
{
  "street": "MAIN",
  "suffix": "ST"
}
```

---

## API Endpoints

### Overview

| Endpoint | Method | Purpose | Authentication |
|----------|--------|---------|----------------|
| `/` | GET | API information | None |
| `/health` | GET | Health check | None |
| `/docs` | GET | Interactive documentation | None |
| `/search/address` | POST | Search properties | None |
| `/tax-summary` | GET | Get tax details | None |

**Note:** This API is currently public and requires no authentication.

---

## Search for Properties

### Endpoint: `POST /search/address`

Search for properties in Fairfax County by address.

### Request Format

**URL:** `https://govtaxcheck.onrender.com/search/address`

**Method:** `POST`

**Headers:**
```
Content-Type: application/json
```

**Body Parameters:**

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `street` | string | **Yes** | Street name | `"MAIN"` |
| `suffix` | string | No | Street suffix | `"ST"`, `"RD"`, `"DR"` |
| `number` | string | No | Street number | `"123"` |
| `unit` | string | No | Unit/Apt number | `"APT 5"` |
| `page_size` | string | No | Results per page (default: 15) | `"25"` |

### Example Request

**Minimal (street only):**
```json
{
  "street": "MAIN"
}
```

**With street suffix:**
```json
{
  "street": "MAIN",
  "suffix": "ST"
}
```

**Complete address:**
```json
{
  "number": "123",
  "street": "MAIN",
  "suffix": "ST",
  "unit": "APT 5"
}
```

### Response Format

```json
{
  "success": true,
  "count": 15,
  "results": [
    {
      "Property Address": "9515 MAIN ST",
      "Owner": "SCHOOL BOARD OF FAIRFAX COUNTY",
      "Map #": "0583 01  0001",
      "Last Sale": "N/A",
      "DetailURL": "https://icare.fairfaxcounty.gov/ffxcare/Datalets/Datalet.aspx?sIndex=0&idx=1"
    },
    {
      "Property Address": "9400 MAIN ST",
      "Owner": "COMBINED PROPERTIES",
      "Map #": "0584 01  0051E",
      "Last Sale": "MAY/25/1982",
      "DetailURL": "https://icare.fairfaxcounty.gov/ffxcare/Datalets/Datalet.aspx?sIndex=0&idx=2"
    }
  ]
}
```

### Response Fields

| Field | Description |
|-------|-------------|
| `success` | Whether the search was successful |
| `count` | Number of properties found |
| `results` | Array of property objects |
| `Property Address` | Full property address |
| `Owner` | Property owner name |
| `Map #` | Fairfax County map reference number |
| `Last Sale` | Date of last property sale |
| `DetailURL` | URL to get tax details (use with `/tax-summary`) |

---

## Get Tax Summary

### Endpoint: `GET /tax-summary`

Get detailed tax information for a specific property.

### Request Format

**URL:** `https://govtaxcheck.onrender.com/tax-summary`

**Method:** `GET`

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `detail_url` | string | **Yes** | DetailURL from search results |

### Example Request

```
https://govtaxcheck.onrender.com/tax-summary?detail_url=https://icare.fairfaxcounty.gov/ffxcare/Datalets/Datalet.aspx?sIndex=0&idx=1
```

**Note:** The `detail_url` parameter should be URL-encoded if calling programmatically.

### Response Format

```json
{
  "success": true,
  "title": "Tax Summary",
  "stub_number": "123456",
  "tax_year_code": "2024",
  "periods": [
    {
      "year": "2024",
      "label": "Current",
      "amount_paid": "$5,234.50",
      "balance_due": "$0.00",
      "amount_paid_decimal": 5234.5,
      "balance_due_decimal": 0.0
    },
    {
      "year": "2023",
      "label": "Prior",
      "amount_paid": "$5,100.00",
      "balance_due": "$0.00",
      "amount_paid_decimal": 5100.0,
      "balance_due_decimal": 0.0
    }
  ],
  "total": {
    "year": "Total",
    "label": "",
    "amount_paid": "$10,334.50",
    "balance_due": "$0.00",
    "amount_paid_decimal": 10334.5,
    "balance_due_decimal": 0.0
  }
}
```

### Response Fields

| Field | Description |
|-------|-------------|
| `success` | Whether the request was successful |
| `title` | Tax summary title |
| `stub_number` | Tax stub number |
| `tax_year_code` | Current tax year code |
| `periods` | Array of tax periods with payment info |
| `total` | Total amounts across all periods |

---

## Using the Interactive Docs

The easiest way to use the API is through the interactive documentation.

### Step-by-Step Guide

**1. Open the Docs**
```
https://govtaxcheck.onrender.com/docs
```

**2. Find the Endpoint**
- Click on "POST /search/address" to expand it

**3. Try It Out**
- Click the "Try it out" button
- Edit the request body:
```json
{
  "street": "MAIN",
  "suffix": "ST"
}
```

**4. Execute**
- Click "Execute" button
- Scroll down to see the response

**5. View Results**
- See the JSON response with property data
- Copy the `DetailURL` from any result

**6. Get Tax Details**
- Click on "GET /tax-summary"
- Click "Try it out"
- Paste the `DetailURL` in the parameter field
- Click "Execute"
- View tax information

---

## Code Examples

### JavaScript / Fetch API

**Search for properties:**
```javascript
async function searchProperties(street, suffix = '') {
  const response = await fetch('https://govtaxcheck.onrender.com/search/address', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      street: street,
      suffix: suffix
    })
  });

  const data = await response.json();
  return data.results;
}

// Usage
searchProperties('MAIN', 'ST').then(properties => {
  console.log(`Found ${properties.length} properties`);
  properties.forEach(prop => {
    console.log(`${prop['Property Address']} - ${prop.Owner}`);
  });
});
```

**Get tax summary:**
```javascript
async function getTaxSummary(detailUrl) {
  const url = new URL('https://govtaxcheck.onrender.com/tax-summary');
  url.searchParams.append('detail_url', detailUrl);

  const response = await fetch(url);
  const data = await response.json();
  return data;
}

// Usage
const detailUrl = "https://icare.fairfaxcounty.gov/ffxcare/Datalets/Datalet.aspx?sIndex=0&idx=1";
getTaxSummary(detailUrl).then(taxData => {
  console.log(`Total Balance Due: ${taxData.total.balance_due}`);
});
```

---

### Python

**Search for properties:**
```python
import requests

def search_properties(street, suffix='', number='', unit=''):
    url = 'https://govtaxcheck.onrender.com/search/address'
    payload = {
        'street': street,
        'suffix': suffix,
        'number': number,
        'unit': unit
    }

    response = requests.post(url, json=payload)
    data = response.json()
    return data['results']

# Usage
properties = search_properties('MAIN', 'ST')
print(f"Found {len(properties)} properties")

for prop in properties:
    print(f"{prop['Property Address']} - {prop['Owner']}")
```

**Get tax summary:**
```python
import requests

def get_tax_summary(detail_url):
    url = 'https://govtaxcheck.onrender.com/tax-summary'
    params = {'detail_url': detail_url}

    response = requests.get(url, params=params)
    return response.json()

# Usage
detail_url = "https://icare.fairfaxcounty.gov/ffxcare/Datalets/Datalet.aspx?sIndex=0&idx=1"
tax_data = get_tax_summary(detail_url)
print(f"Total Balance Due: {tax_data['total']['balance_due']}")
```

---

### PowerShell

**Search for properties:**
```powershell
function Search-Properties {
    param(
        [string]$Street,
        [string]$Suffix = ""
    )

    $body = @{
        street = $Street
        suffix = $Suffix
    } | ConvertTo-Json

    $response = Invoke-RestMethod `
        -Method Post `
        -Uri "https://govtaxcheck.onrender.com/search/address" `
        -ContentType "application/json" `
        -Body $body

    return $response.results
}

# Usage
$properties = Search-Properties -Street "MAIN" -Suffix "ST"
Write-Host "Found $($properties.Count) properties"

foreach ($prop in $properties) {
    Write-Host "$($prop.'Property Address') - $($prop.Owner)"
}
```

**Get tax summary:**
```powershell
function Get-TaxSummary {
    param([string]$DetailUrl)

    $uri = "https://govtaxcheck.onrender.com/tax-summary?detail_url=$DetailUrl"
    $response = Invoke-RestMethod -Uri $uri

    return $response
}

# Usage
$detailUrl = "https://icare.fairfaxcounty.gov/ffxcare/Datalets/Datalet.aspx?sIndex=0&idx=1"
$taxData = Get-TaxSummary -DetailUrl $detailUrl
Write-Host "Total Balance Due: $($taxData.total.balance_due)"
```

---

### cURL (Command Line)

**Search for properties:**
```bash
curl -X POST "https://govtaxcheck.onrender.com/search/address" \
  -H "Content-Type: application/json" \
  -d '{
    "street": "MAIN",
    "suffix": "ST"
  }'
```

**Get tax summary:**
```bash
curl -X GET "https://govtaxcheck.onrender.com/tax-summary?detail_url=https://icare.fairfaxcounty.gov/ffxcare/Datalets/Datalet.aspx?sIndex=0&idx=1"
```

---

## Common Use Cases

### Use Case 1: Find All Properties on a Street

**Goal:** Get all properties on Main Street

**Steps:**
1. Search with just the street name
2. Loop through results

**Example:**
```javascript
const response = await fetch('https://govtaxcheck.onrender.com/search/address', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ street: 'MAIN' })
});

const data = await response.json();
console.log(`Found ${data.count} properties on Main Street`);
```

---

### Use Case 2: Check Tax Status for Specific Address

**Goal:** Find a specific property and check if taxes are owed

**Steps:**
1. Search with full address details
2. Get the first result's DetailURL
3. Fetch tax summary
4. Check balance_due

**Example:**
```python
import requests

# Step 1: Search
search_response = requests.post(
    'https://govtaxcheck.onrender.com/search/address',
    json={'number': '9515', 'street': 'MAIN', 'suffix': 'ST'}
)
results = search_response.json()['results']

if results:
    # Step 2: Get detail URL
    detail_url = results[0]['DetailURL']

    # Step 3: Get tax summary
    tax_response = requests.get(
        'https://govtaxcheck.onrender.com/tax-summary',
        params={'detail_url': detail_url}
    )
    tax_data = tax_response.json()

    # Step 4: Check balance
    balance = tax_data['total']['balance_due']
    print(f"Balance Due: {balance}")
```

---

### Use Case 3: Build a Property Search Web App

**Goal:** Create a simple web form to search properties

**Example HTML + JavaScript:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Fairfax Property Search</title>
</head>
<body>
    <h1>Search Fairfax County Properties</h1>

    <form id="searchForm">
        <input type="text" id="street" placeholder="Street Name" required>
        <input type="text" id="suffix" placeholder="Suffix (ST, RD, etc)">
        <button type="submit">Search</button>
    </form>

    <div id="results"></div>

    <script>
        document.getElementById('searchForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            const street = document.getElementById('street').value;
            const suffix = document.getElementById('suffix').value;

            const response = await fetch('https://govtaxcheck.onrender.com/search/address', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ street, suffix })
            });

            const data = await response.json();

            let html = `<h2>Found ${data.count} properties</h2><ul>`;
            data.results.forEach(prop => {
                html += `<li>${prop['Property Address']} - ${prop.Owner}</li>`;
            });
            html += '</ul>';

            document.getElementById('results').innerHTML = html;
        });
    </script>
</body>
</html>
```

---

### Use Case 4: Export Property Data to CSV

**Goal:** Search for properties and save to CSV file

**Example Python:**
```python
import requests
import csv

def export_properties_to_csv(street, suffix, filename):
    # Search
    response = requests.post(
        'https://govtaxcheck.onrender.com/search/address',
        json={'street': street, 'suffix': suffix}
    )

    properties = response.json()['results']

    # Write to CSV
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Property Address', 'Owner', 'Map #', 'Last Sale']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for prop in properties:
            writer.writerow({
                'Property Address': prop.get('Property Address', ''),
                'Owner': prop.get('Owner', ''),
                'Map #': prop.get('Map #', ''),
                'Last Sale': prop.get('Last Sale', '')
            })

    print(f"Exported {len(properties)} properties to {filename}")

# Usage
export_properties_to_csv('MAIN', 'ST', 'main_street_properties.csv')
```

---

## Troubleshooting

### Issue: Slow First Request (~50 seconds)

**Cause:** Free tier on Render spins down after 15 minutes of inactivity.

**Solution:**
- First request wakes up the server (slow)
- Subsequent requests are fast
- Optional: Use [UptimeRobot](https://uptimerobot.com/) to keep it warm

---

### Issue: CORS Error in Browser

**Symptom:**
```
Access to fetch at 'https://govtaxcheck.onrender.com' from origin 'http://localhost'
has been blocked by CORS policy
```

**Solution:**
CORS is already enabled for all origins. This shouldn't happen, but if it does:
- Make sure you're using HTTPS in the API URL
- Check that `Content-Type: application/json` header is set

---

### Issue: "street is required" Error

**Cause:** Missing required `street` parameter

**Solution:**
```json
{
  "street": "MAIN"  // Required!
}
```

The `street` field must be provided, even if empty string.

---

### Issue: No Results Found

**Cause:** No matching properties in Fairfax County

**Solutions:**
- Try searching with just street name (no number)
- Remove the suffix and try again
- Try a different street
- Make sure you're searching for Fairfax County, VA properties

---

### Issue: Tax Summary Not Found

**Cause:** Some properties don't have tax data available

**Solution:**
This is expected for certain property types (government buildings, etc.). Try a different property.

---

### Issue: Invalid DetailURL

**Cause:** DetailURL parameter is malformed or missing

**Solution:**
- Make sure you're passing the full URL from search results
- URL-encode the parameter if calling programmatically
- Don't modify the DetailURL - use it exactly as returned

---

## Rate Limiting

**Current Status:** No rate limiting

The API currently has no rate limits, but please be respectful:
- Don't make excessive requests
- Cache results when possible
- Use reasonable page_size values

Future versions may add rate limiting if needed.

---

## Support & Feedback

### Need Help?

1. **Interactive Docs:** https://govtaxcheck.onrender.com/docs
2. **Health Check:** https://govtaxcheck.onrender.com/health
3. **GitHub:** https://github.com/mattsegura/govtaxcheck

### Report Issues

If you encounter bugs or have suggestions:
- Check the troubleshooting section above
- Open an issue on GitHub
- Include request/response examples

---

## API Limits & Fair Use

**Free Tier Limitations:**
- Service may sleep after 15 minutes of inactivity
- First request after sleep takes ~50 seconds
- No guaranteed uptime (free tier)

**Fair Use Policy:**
- Don't abuse the API with excessive requests
- Cache results when appropriate
- Be respectful of the underlying Fairfax County website

---

## Quick Reference

### Endpoints Summary

```
GET  /                 - API info
GET  /health          - Health check
GET  /docs            - Interactive docs
POST /search/address  - Search properties
GET  /tax-summary     - Get tax details
```

### Minimal Search Example

```bash
curl -X POST "https://govtaxcheck.onrender.com/search/address" \
  -H "Content-Type: application/json" \
  -d '{"street":"MAIN"}'
```

### Complete Workflow

1. **Search** → Get properties
2. **Extract** → Get DetailURL from results
3. **Tax Summary** → Get tax details using DetailURL
4. **Use Data** → Process in your application

---

## Additional Resources

- **Live API:** https://govtaxcheck.onrender.com
- **Interactive Docs:** https://govtaxcheck.onrender.com/docs
- **GitHub Repository:** https://github.com/mattsegura/govtaxcheck
- **Fairfax County iCare:** https://icare.fairfaxcounty.gov

---

**Happy searching!** 🏘️📊
