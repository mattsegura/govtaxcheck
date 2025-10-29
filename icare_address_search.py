"""
Interactive CLI for county property searches.

Right now only Fairfax County iCare is wired up, but the menu-driven
workflow makes it easy to plug in more counties later. The script prompts
for county selection, asks for the address, and prints tax summaries.

Install dependencies first:
    pip install requests beautifulsoup4
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

SEARCH_URL = "https://icare.fairfaxcounty.gov/ffxcare/search/CommonSearch.aspx?mode=ADDRESS"
MAP_NUMBER_SEARCH_URL = "https://icare.fairfaxcounty.gov/ffxcare/search/CommonSearch.aspx?mode=PARID"


def collect_form_fields(html: str) -> Dict[str, str]:
    """Return a mapping of all form input names to their values."""
    soup = BeautifulSoup(html, "html.parser")
    fields: Dict[str, str] = {}
    for tag in soup.select("input[name]"):
        name = tag.get("name")
        if not name:
            continue
        fields[name] = tag.get("value", "")
    return fields


def _extract_detail_url(tr: BeautifulSoup) -> Optional[str]:
    """Extract the detail URL embedded in the row's onclick handler."""
    onclick = tr.get("onclick") or ""
    marker = "selectSearchRow('"
    if marker not in onclick:
        return None
    start = onclick.index(marker) + len(marker)
    end = onclick.find("')", start)
    if end == -1:
        return None
    relative = onclick[start:end]
    return requests.compat.urljoin(SEARCH_URL, relative)


def parse_results_table(html: str) -> List[Dict[str, str]]:
    """Parse the address results grid into a list of dictionaries."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one("table#searchResults") or soup.select_one("table.rgMasterTable")
    if not table:
        return []

    headers: List[Optional[str]] = []
    for th in table.select("thead tr th"):
        text = th.get_text(" ", strip=True)
        text = text.replace("\u25b2", "").replace("\u25bc", "").strip()
        headers.append(text or None)

    rows: List[Dict[str, str]] = []
    for tr in table.select("tbody tr"):
        cells = [td.get_text(" ", strip=True) for td in tr.select("td")]
        if not cells:
            continue
        # Drop leading checkbox column if present.
        if len(cells) > len(headers):
            cells = cells[-len(headers):]
        if len(cells) != len(headers):
            continue
        row: Dict[str, str] = {}
        for header, cell in zip(headers, cells):
            if header:
                row[header] = cell
        detail = _extract_detail_url(tr)
        if detail:
            row["DetailURL"] = detail
        rows.append(row)
    return rows


def search_fairfax_address(
    number: str,
    street: str,
    suffix: str = "",
    unit: str = "",
    page_size: str = "15",
    session: requests.Session | None = None,
) -> Tuple[List[Dict[str, str]], str]:
    """Perform an address search and return parsed rows plus the raw HTML."""
    session = session or requests.Session()

    initial = session.get(SEARCH_URL, timeout=30)
    initial.raise_for_status()

    payload = collect_form_fields(initial.text)
    payload.update(
        {
            "inpNumber": number,
            "inpStreet": street,
            "inpSuffix1": suffix,
            "inpUnit": unit,
            "hdAction": "Search",
            "PageNum": "1",
            "PageSize": page_size,
            "selPageSize": page_size,
        }
    )

    response = session.post(SEARCH_URL, data=payload, timeout=30)
    response.raise_for_status()
    return parse_results_table(response.text), response.text


def search_fairfax_map_number(
    map_number: str,
    session: requests.Session | None = None,
) -> Tuple[List[Dict[str, str]], str]:
    """Perform a map number search and return parsed rows plus the raw HTML.

    Map number format: "0812 03 0026" or "0812030026" (will be normalized to "0812 03 0026")
    """
    session = session or requests.Session()

    # Normalize map number - remove all spaces
    map_clean = map_number.replace(" ", "")

    # If we have exactly 10 digits, format it as: XXXX XX XXXX (single spaces)
    if len(map_clean) == 10 and map_clean.isdigit():
        map_formatted = f"{map_clean[0:4]} {map_clean[4:6]} {map_clean[6:10]}"
    else:
        # Use as-is if it doesn't match expected format
        map_formatted = map_number

    initial = session.get(MAP_NUMBER_SEARCH_URL, timeout=30)
    initial.raise_for_status()

    payload = collect_form_fields(initial.text)
    payload.update(
        {
            "inpParid": map_formatted,
            "hdAction": "Search",
            "PageNum": "1",
            "PageSize": "15",
            "selPageSize": "15",
        }
    )

    response = session.post(MAP_NUMBER_SEARCH_URL, data=payload, timeout=30)
    response.raise_for_status()
    return parse_results_table(response.text), response.text


def parse_currency(value: str) -> Decimal:
    """Convert Fairfax currency strings like '$.00' or '-$59,026.66' to Decimals."""
    cleaned = value.replace("$", "").replace(",", "").strip()
    if cleaned in {"", ".", ".00"}:
        return Decimal("0")
    if cleaned.startswith("-."):
        cleaned = "-0" + cleaned[1:]
    elif cleaned.startswith("."):
        cleaned = "0" + cleaned
    try:
        return Decimal(cleaned)
    except InvalidOperation as exc:
        raise ValueError(f"Unable to parse currency value '{value}'") from exc


def format_currency(amount: Decimal) -> str:
    sign = "-" if amount < 0 else ""
    return f"{sign}${abs(amount):,.2f}"


def extract_fairfax_tax_summary(html: str) -> Dict[str, object]:
    """Return structured tax summary data from the Fairfax tax detail page."""
    soup = BeautifulSoup(html, "html.parser")

    stub_number = None
    stub_div = soup.select_one("div[name='TAX_STUB']")
    if stub_div:
        data_cells = stub_div.select("table:nth-of-type(2) td.DataletData")
        if data_cells:
            stub_number = data_cells[0].get_text(strip=True)

    summary_div = soup.select_one("div[name='TAX_SUM']")
    if not summary_div:
        raise ValueError("Tax summary section not found on the page.")

    heading_table = summary_div.find("table")
    title = heading_table.get_text(strip=True) if heading_table else "Tax Summary"

    data_table = summary_div.find("table", id=lambda v: v and v.startswith("Summary"))
    if not data_table:
        raise ValueError("Summary table not found inside tax section.")

    header_cells = data_table.find("tr").find_all("td")
    headers = [cell.get_text(strip=True) for cell in header_cells]

    periods: List[Dict[str, object]] = []
    total_entry: Optional[Dict[str, object]] = None

    for tr in data_table.find_all("tr")[1:]:
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(cells) != len(headers):
            continue
        record = dict(zip(headers, cells))
        entry = {
            "year": record.get("Year", ""),
            "label": record.get("", ""),
            "amount_paid": parse_currency(record.get("Amount Paid", "$0")),
            "balance_due": parse_currency(record.get("Balance Due", "$0")),
            "raw": record,
        }
        if entry["year"].strip().lower().startswith("total"):
            total_entry = entry
        else:
            periods.append(entry)

    if total_entry is None:
        total_entry = {
            "year": "Total",
            "label": "",
            "amount_paid": Decimal("0"),
            "balance_due": Decimal("0"),
            "raw": {},
        }

    for entry in periods + [total_entry]:
        entry["amount_paid_display"] = format_currency(entry["amount_paid"])
        entry["balance_due_display"] = format_currency(entry["balance_due"])

    tax_year_code = ""
    tax_year_field = soup.select_one("#hdTaxYear")
    if tax_year_field and tax_year_field.has_attr("value"):
        tax_year_code = tax_year_field["value"]

    return {
        "title": title,
        "stub_number": stub_number,
        "periods": periods,
        "total": total_entry,
        "tax_year_code": tax_year_code,
    }


def fetch_fairfax_tax_summary(session: requests.Session, detail_url: str) -> Dict[str, object]:
    """Load the tax detail page for a property and return parsed summary data."""
    profile_resp = session.get(detail_url, timeout=30)
    profile_resp.raise_for_status()

    soup = BeautifulSoup(profile_resp.text, "html.parser")
    tax_link = soup.select_one("div#sidemenu a[href*='mode=tax_details']")
    if tax_link and tax_link.has_attr("href"):
        tax_href = tax_link["href"]
        tax_url = urljoin(detail_url, tax_href)
    else:
        separator = "&" if "?" in detail_url else "?"
        tax_url = f"{detail_url}{separator}mode=tax_details"

    tax_resp = session.get(tax_url, timeout=30)
    tax_resp.raise_for_status()
    return extract_fairfax_tax_summary(tax_resp.text)


def prompt_choice(options: Dict[str, str]) -> str:
    """Prompt the user to choose from a mapping of option id -> label."""
    print("Choose a county:")
    for key, label in options.items():
        print(f"  [{key}] {label}")
    while True:
        choice = input("Selection: ").strip()
        if choice in options:
            return choice
        print("Please enter one of the listed options.")


def prompt_address() -> Tuple[str, str, str, str]:
    """Collect address search inputs from the user."""
    number = input("Street number (optional): ").strip()
    street = ""
    while not street:
        street = input("Street name (required): ").strip().upper()
        if not street:
            print("Street name is required.")
    suffix = input("Street suffix (e.g., RD, DR) (optional): ").strip().upper()
    unit = input("Unit / Apt (optional): ").strip()
    return number, street, suffix, unit


def prompt_result_selection(count: int) -> Optional[int]:
    """Ask the user to select a result index or restart the search."""
    if count <= 0:
        return None
    prompt = f"Select a property [1-{count}] or 'r' to refine search: "
    while True:
        raw = input(prompt).strip().lower()
        if raw in {"r", "restart", "rescan"}:
            return None
        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= count:
                return idx - 1
        print("Please enter a valid option.")


def prompt_yes_no(message: str, default: bool = False) -> bool:
    """Prompt user for yes/no, returning True for yes."""
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        raw = input(f"{message} {suffix} ").strip().lower()
        if not raw:
            return default
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False
        print("Please respond with 'y' or 'n'.")


def display_search_results(rows: List[Dict[str, str]]) -> None:
    print("\nSearch Results:")
    for idx, row in enumerate(rows, start=1):
        address = row.get("Property Address", "Unknown address").strip()
        owner = row.get("Owner", "Unknown owner").strip()
        map_num = row.get("Map #", "").strip()
        print(f"  [{idx}] {address} — {owner} (Map {map_num})")
    print()


def display_tax_summary(property_row: Dict[str, str], summary: Dict[str, object]) -> None:
    print("\nSelected Property:")
    print(f"  Address: {property_row.get('Property Address', 'N/A')}")
    print(f"  Owner:   {property_row.get('Owner', 'N/A')}")
    print(f"  Map #:   {property_row.get('Map #', 'N/A')}")
    if summary.get("stub_number"):
        print(f"  Stub #:  {summary['stub_number']}")

    print(f"\n{summary.get('title', 'Tax Summary')}")
    for entry in summary.get("periods", []):
        label = entry.get("label", "")
        label_text = f" ({label})" if label else ""
        print(
            f"  - {entry.get('year', '')}{label_text}: "
            f"Balance Due {entry['balance_due_display']} | "
            f"Amount Paid {entry['amount_paid_display']}"
        )

    total = summary.get("total", {})
    total_due = total.get("balance_due_display", "$0.00")
    print(f"\nTotal Balance Due: {total_due}\n")


def run_fairfax_cli() -> None:
    session = requests.Session()

    while True:
        number, street, suffix, unit = prompt_address()
        try:
            results, _ = search_fairfax_address(
                number=number,
                street=street,
                suffix=suffix,
                unit=unit,
                session=session,
            )
        except requests.RequestException as exc:
            print(f"Search failed: {exc}")
            if prompt_yes_no("Try another search?", default=True):
                continue
            return

        if not results:
            print("No matching properties found.")
            if prompt_yes_no("Would you like to search again?", default=True):
                continue
            return

        display_search_results(results)
        selection = prompt_result_selection(len(results))
        if selection is None:
            continue

        chosen = results[selection]
        try:
            summary = fetch_fairfax_tax_summary(session, chosen["DetailURL"])
        except requests.RequestException as exc:
            print(f"Failed to load tax details: {exc}")
            if prompt_yes_no("Search for another property?", default=True):
                continue
            return
        except ValueError as exc:
            print(f"Could not parse tax details: {exc}")
            if prompt_yes_no("Search for another property?", default=True):
                continue
            return

        display_tax_summary(chosen, summary)

        if not prompt_yes_no("Look up another property?"):
            break


def main() -> None:
    counties = {
        "1": "Fairfax County, VA (iCare)",
    }
    selection = prompt_choice(counties)

    if selection == "1":
        run_fairfax_cli()
    else:
        raise RuntimeError("Unhandled county selection.")


if __name__ == "__main__":
    main()
