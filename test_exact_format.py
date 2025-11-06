#!/usr/bin/env python3
"""Test exact map number format from curl request"""

import requests
from bs4 import BeautifulSoup
from icare_address_search import MAP_NUMBER_SEARCH_URL, collect_form_fields

def test_exact_search(map_number, format_description):
    """Test with exact format"""
    session = requests.Session()

    print(f"\nTesting: {format_description}")
    print(f"Map number: '{map_number}'")

    # Get initial page
    initial = session.get(MAP_NUMBER_SEARCH_URL, timeout=30)
    initial.raise_for_status()

    # Collect form fields
    payload = collect_form_fields(initial.text)
    payload.update({
        "inpParid": map_number,
        "hdAction": "Search",
        "PageNum": "1",
        "PageSize": "15",
        "selPageSize": "15",
    })

    # Send search request
    response = session.post(MAP_NUMBER_SEARCH_URL, data=payload, timeout=30)
    response.raise_for_status()

    # Parse results
    soup = BeautifulSoup(response.text, "html.parser")

    # Look for results table
    table = soup.find("table", {"id": "searchResults"})
    if table:
        results = table.select("tbody tr")
        # Filter out empty rows
        results = [r for r in results if r.find("td")]

        if results:
            print(f"✓ Found {len(results)} result(s)!")
            # Get first result details
            first_result = results[0]
            cells = first_result.find_all("td")
            if len(cells) >= 5:
                owner = cells[0].get_text(strip=True)
                address = cells[1].get_text(strip=True)
                map_num = cells[4].get_text(strip=True) if len(cells) > 4 else "N/A"
                print(f"  Owner: {owner}")
                print(f"  Address: {address}")
                print(f"  Map # (in results): '{map_num}'")
            return True
        else:
            print("✗ No results found (empty table)")
    else:
        print("✗ No results table in response")

    return False

# Test the working map number with different formats
print("="*60)
print("Testing WORKING map number: 0812030026")
print("="*60)

# From curl request - single spaces
test_exact_search("0812 03 0026", "Single spaces (from curl)")

# What we see in results - double space
test_exact_search("0812 03  0026", "Double space (from HTML results)")

# No spaces
test_exact_search("0812030026", "No spaces")

print("\n" + "="*60)
print("Testing PROBLEMATIC map number: 1202010001")
print("="*60)

# Try different formats for the problematic number
test_exact_search("1202 01 0001", "Single spaces")
test_exact_search("1202 01  0001", "Double space")
test_exact_search("1202010001", "No spaces")

# Maybe it needs leading zeros or different grouping?
test_exact_search("12020 10 001", "Different grouping 5-2-3")
test_exact_search("120201 0001", "Different grouping 6-4")