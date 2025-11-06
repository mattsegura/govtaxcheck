#!/usr/bin/env python3
"""Test map number search directly"""

import requests
from icare_address_search import search_fairfax_map_number, MAP_NUMBER_SEARCH_URL, collect_form_fields
from bs4 import BeautifulSoup

def test_map_search_debug(map_number):
    """Test with detailed debugging"""
    session = requests.Session()

    print(f"\nTesting map number: {map_number}")
    print(f"URL: {MAP_NUMBER_SEARCH_URL}")

    # Get initial page
    initial = session.get(MAP_NUMBER_SEARCH_URL, timeout=30)
    initial.raise_for_status()
    print(f"Initial page status: {initial.status_code}")

    # Parse the form to see what fields exist
    soup = BeautifulSoup(initial.text, "html.parser")
    input_field = soup.find("input", {"name": "inpParid"})
    if input_field:
        print(f"Found inpParid field with value: '{input_field.get('value', '')}'")

    # Collect form fields
    payload = collect_form_fields(initial.text)
    print(f"\nForm fields collected: {len(payload)} fields")

    # Check specific fields
    for key in ["inpParid", "__VIEWSTATE", "__EVENTVALIDATION"]:
        if key in payload:
            val = payload[key]
            if len(str(val)) > 100:
                print(f"  {key}: [long value, {len(str(val))} chars]")
            else:
                print(f"  {key}: '{val}'")

    # Format the map number
    map_clean = map_number.replace(" ", "")
    if len(map_clean) == 10 and map_clean.isdigit():
        map_formatted = f"{map_clean[0:4]} {map_clean[4:6]} {map_clean[6:10]}"
    else:
        map_formatted = map_number

    print(f"\nFormatted map number: '{map_formatted}'")

    # Update payload
    payload.update({
        "inpParid": map_formatted,
        "hdAction": "Search",
        "PageNum": "1",
        "PageSize": "15",
        "selPageSize": "15",
    })

    print("\nSending POST request...")
    response = session.post(MAP_NUMBER_SEARCH_URL, data=payload, timeout=30)
    print(f"Response status: {response.status_code}")

    # Check if we got results
    soup = BeautifulSoup(response.text, "html.parser")

    # Look for the results table
    table = soup.select_one("table.SearchResults")
    if table:
        rows = table.select("tr")
        print(f"Found results table with {len(rows)} rows")
    else:
        print("No results table found")

    # Check for error messages
    error_div = soup.select_one("div.validation-summary-errors")
    if error_div:
        print(f"Error message: {error_div.get_text(strip=True)}")

    # Check for no results message
    no_results = soup.find(text=lambda t: "No results found" in t if t else False)
    if no_results:
        print("Found 'No results found' message")

    # Save the response for manual inspection
    with open("debug_response.html", "w") as f:
        f.write(response.text)
    print("\nResponse saved to debug_response.html")

    return response.text

# Test with the map number from the screenshot
test_map_search_debug("1202010001")

# Also test with the working map number
print("\n" + "="*50)
test_map_search_debug("0812030026")