#!/usr/bin/env python3
"""Direct test of map number search on Fairfax website"""

import requests
from bs4 import BeautifulSoup
from icare_address_search import MAP_NUMBER_SEARCH_URL, collect_form_fields

def test_map_formats(base_number):
    """Test different formats of a map number"""
    formats_to_test = [
        base_number,  # As provided: 1202010001
        f"{base_number[0:4]} {base_number[4:6]} {base_number[6:10]}",  # Single space: 1202 01 0001
        f"{base_number[0:4]} {base_number[4:6]}  {base_number[6:10]}",  # Double space: 1202 01  0001
        f"{base_number[0:4]}-{base_number[4:6]}-{base_number[6:10]}",  # Dashes: 1202-01-0001
        f"{base_number[0:4]}{base_number[4:6]} {base_number[6:10]}",  # Space after 6: 120201 0001
    ]

    session = requests.Session()

    for format_test in formats_to_test:
        print(f"\nTesting format: '{format_test}'")

        # Get initial page
        initial = session.get(MAP_NUMBER_SEARCH_URL, timeout=30)
        initial.raise_for_status()

        # Collect form fields
        payload = collect_form_fields(initial.text)
        payload.update({
            "inpParid": format_test,
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

        # Look for results
        table = soup.find("table", {"id": "searchResults"})
        if table:
            results = table.select("tbody tr.SearchResults")
            if results:
                print(f"  ✓ Found {len(results)} result(s)!")
                # Get first result details
                first_result = results[0]
                cells = first_result.find_all("td")
                if len(cells) >= 5:
                    owner = cells[0].get_text(strip=True)
                    address = cells[1].get_text(strip=True)
                    map_num = cells[4].get_text(strip=True) if len(cells) > 4 else "N/A"
                    print(f"    Owner: {owner}")
                    print(f"    Address: {address}")
                    print(f"    Map #: {map_num}")
                return format_test  # Return successful format
            else:
                print(f"  ✗ No results found")
        else:
            print(f"  ✗ No results table in response")

        # Check for error messages
        error_msgs = soup.find_all(text=lambda t: t and ("no records" in t.lower() or "not found" in t.lower()))
        if error_msgs:
            print(f"  Error message: {error_msgs[0].strip()}")

    return None

# Test the map number from the screenshot
print("Testing MAP #: 1202 01 0001")
print("="*50)

successful_format = test_map_formats("1202010001")

if successful_format:
    print(f"\n✓ Success! The working format is: '{successful_format}'")
else:
    print("\n✗ No working format found. The map number might not exist in the system.")

# Also test with our known working number
print("\n" + "="*50)
print("Testing known working MAP #: 0812 03 0026")
print("="*50)

successful_format = test_map_formats("0812030026")
if successful_format:
    print(f"\n✓ Success! The working format is: '{successful_format}'")