#!/usr/bin/env python3
"""
Travis County, TX property search functions.
"""

import requests
from typing import List, Dict, Tuple, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

# Travis County search URL
TRAVIS_SEARCH_URL = "https://travis.go2gov.net/cart/responsive/quickSearch.do"
TRAVIS_PROPERTY_BASE = "https://travis.go2gov.net/cart/responsive/"

def search_travis_property(
    property_id: str,
    session: requests.Session | None = None,
) -> Tuple[List[Dict[str, str]], str]:
    """Search for a property in Travis County by property ID.

    Args:
        property_id: The property ID to search for (e.g., "01507011040000")
        session: Optional requests session to use

    Returns:
        Tuple of (list of property results, raw HTML response)
    """
    session = session or requests.Session()

    # Clean the property ID (remove any spaces or special characters)
    property_id = property_id.strip().replace(" ", "").replace("-", "")

    print(f"[DEBUG] Searching Travis County for property ID: '{property_id}'")

    # Prepare the form data based on the curl request
    data = {
        'formViewMode': 'responsive',
        'criteria.searchStatus': '1',
        'pager.pageSize': '10',
        'pager.pageNumber': '1',
        'criteria.heuristicSearch': property_id
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://travis.go2gov.net',
        'Referer': 'https://travis.go2gov.net/cart/responsive/quickSearch.do'
    }

    try:
        # Send the search request
        response = session.post(TRAVIS_SEARCH_URL, data=data, headers=headers, timeout=30)
        response.raise_for_status()

        # Parse the results
        results = parse_travis_results(response.text)
        print(f"[DEBUG] Found {len(results)} results")

        return results, response.text

    except requests.RequestException as e:
        print(f"[ERROR] Failed to search Travis County: {e}")
        return [], ""


def parse_travis_results(html: str) -> List[Dict[str, str]]:
    """Parse the Travis County search results HTML.

    Args:
        html: The HTML response from the search

    Returns:
        List of dictionaries containing property information
    """
    soup = BeautifulSoup(html, "html.parser")
    results = []

    # Look for the results table or list
    # Travis County uses a different format - need to inspect the actual HTML

    # First, check if there are any results
    no_results = soup.find(text=re.compile(r"No properties found", re.IGNORECASE))
    if no_results:
        print("[DEBUG] No properties found message detected")
        return []

    # Try to find property results - Travis County may use different selectors
    # Look for common patterns in property search results

    # Try finding by class names that might contain results
    result_containers = (
        soup.find_all("div", class_="property-result") or
        soup.find_all("tr", class_="result-row") or
        soup.find_all("div", class_="search-result") or
        soup.find_all("div", class_="row result") or
        soup.find_all("div", {"class": re.compile(r"result", re.I)})
    )

    # Also check for table-based results
    if not result_containers:
        table = soup.find("table", {"class": re.compile(r"result", re.I)}) or \
                soup.find("table", {"id": re.compile(r"result", re.I)})
        if table:
            result_containers = table.find_all("tr")[1:]  # Skip header row

    # Parse each result
    for container in result_containers:
        property_data = {}

        # Try to extract common fields
        # Property ID
        prop_id = container.find(text=re.compile(r"\d{14}"))  # 14-digit property ID
        if prop_id:
            property_data["Property ID"] = prop_id.strip()

        # Owner name
        owner_elem = container.find(text=re.compile(r"owner", re.I))
        if owner_elem and owner_elem.parent:
            owner_text = owner_elem.parent.get_text(strip=True)
            property_data["Owner"] = owner_text.replace("Owner:", "").strip()

        # Address
        address_elem = container.find(text=re.compile(r"\d+.*(?:st|rd|ave|dr|ln|way|ct)", re.I))
        if address_elem:
            property_data["Address"] = address_elem.strip()

        # Try to find a link to property details
        detail_link = container.find("a", href=True)
        if detail_link:
            href = detail_link.get("href", "")
            if href:
                property_data["DetailURL"] = urljoin(TRAVIS_PROPERTY_BASE, href)

        if property_data:
            results.append(property_data)

    # If no structured results found, try to extract from the page text
    if not results:
        # Look for property information in a more generic way
        property_section = soup.find("div", {"id": "propertyInfo"}) or \
                          soup.find("div", {"class": "property-info"})

        if property_section:
            property_data = {}

            # Extract text content and parse it
            text_content = property_section.get_text()
            lines = [line.strip() for line in text_content.split('\n') if line.strip()]

            for line in lines:
                if re.match(r"\d{14}", line):
                    property_data["Property ID"] = line
                elif "owner" in line.lower():
                    property_data["Owner"] = line.split(":", 1)[-1].strip()
                elif re.search(r"\d+.*(?:st|rd|ave|dr|ln|way|ct)", line, re.I):
                    property_data["Address"] = line

            if property_data:
                results.append(property_data)

    return results


def fetch_travis_property_details(
    detail_url: str,
    session: requests.Session | None = None
) -> Dict[str, object]:
    """Fetch detailed property information from Travis County.

    Args:
        detail_url: URL to the property detail page
        session: Optional requests session

    Returns:
        Dictionary containing property details
    """
    session = session or requests.Session()

    try:
        response = session.get(detail_url, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        details = {}

        # Extract property details from the page
        # This will need to be customized based on Travis County's actual HTML structure

        # Look for common property detail patterns
        detail_sections = soup.find_all(["div", "section", "table"],
                                       {"class": re.compile(r"detail|property|info", re.I)})

        for section in detail_sections:
            # Extract key-value pairs
            rows = section.find_all(["tr", "div", "dl"])
            for row in rows:
                # Try to find label-value pairs
                label = row.find(["th", "dt", "span", "label"])
                value = row.find(["td", "dd", "span"])

                if label and value:
                    key = label.get_text(strip=True).rstrip(":")
                    val = value.get_text(strip=True)
                    if key and val:
                        details[key] = val

        return details

    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch property details: {e}")
        return {}


# Test function
if __name__ == "__main__":
    # Test with the provided property ID
    test_id = "01507011040000"
    print(f"Testing Travis County search with property ID: {test_id}")

    results, html = search_travis_property(test_id)

    if results:
        print(f"\nFound {len(results)} result(s):")
        for i, result in enumerate(results, 1):
            print(f"\nResult {i}:")
            for key, value in result.items():
                print(f"  {key}: {value}")
    else:
        print("\nNo results found")

        # Save HTML for debugging
        with open("travis_search_debug.html", "w") as f:
            f.write(html)
        print("HTML saved to travis_search_debug.html for debugging")