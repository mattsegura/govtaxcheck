"""
FastAPI application for multi-county property and tax searches.

Supports multiple counties:
- Fairfax County, VA
- Mecklenburg County, NC (coming soon)

Endpoints:
- GET /counties - List available counties
- POST /search/address - Search properties by address
- GET /search/map/{map_number} - Search by map number
- GET /tax-summary - Get tax summary for a property

Install dependencies:
    pip install fastapi uvicorn requests beautifulsoup4

Run the server:
    uvicorn api:app --reload
"""

from __future__ import annotations

from decimal import Decimal
from typing import Dict, List, Optional
from urllib.parse import unquote

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import requests

from icare_address_search import (
    search_fairfax_address,
    search_fairfax_map_number,
    fetch_fairfax_tax_summary,
    parse_currency,
    format_currency,
)

app = FastAPI(
    title="Multi-County Property Search API",
    description="API for searching properties and retrieving tax information from multiple counties",
    version="2.0.0",
)

# Add CORS middleware to allow requests from web browsers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins - restrict in production if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# County Configuration
SUPPORTED_COUNTIES = {
    "fairfax-va": {
        "id": "fairfax-va",
        "name": "Fairfax County",
        "state": "Virginia",
        "state_abbr": "VA",
        "features": ["address_search", "map_search", "tax_summary"],
        "description": "Fairfax County, Virginia property and tax search"
    },
    "mecklenburg-nc": {
        "id": "mecklenburg-nc",
        "name": "Mecklenburg County",
        "state": "North Carolina",
        "state_abbr": "NC",
        "features": ["parcel_search"],
        "description": "Mecklenburg County, North Carolina property search via parcel ID (coming soon)",
        "status": "coming_soon"
    }
}


# Request/Response Models
class AddressSearchRequest(BaseModel):
    """Request model for address search."""
    county: str = Field(default="fairfax-va", description="County ID (e.g., 'fairfax-va', 'mecklenburg-nc')")
    number: str = Field(default="", description="Street number")
    street: str = Field(..., description="Street name (required)")
    suffix: str = Field(default="", description="Street suffix (e.g., RD, DR)")
    unit: str = Field(default="", description="Unit/Apartment number")
    page_size: str = Field(default="15", description="Number of results per page")

    class Config:
        json_schema_extra = {
            "example": {
                "number": "123",
                "street": "MAIN",
                "suffix": "ST",
                "unit": "",
                "page_size": "15"
            }
        }


class PropertyResult(BaseModel):
    """Property search result."""
    property_address: Optional[str] = Field(None, alias="Property Address")
    owner: Optional[str] = Field(None, alias="Owner")
    map_number: Optional[str] = Field(None, alias="Map #")
    detail_url: Optional[str] = Field(None, alias="DetailURL")
    raw_data: Dict[str, str] = Field(default_factory=dict)

    class Config:
        populate_by_name = True


class SearchResponse(BaseModel):
    """Response model for address search."""
    success: bool
    count: int
    results: List[Dict[str, str]]


class TaxPeriod(BaseModel):
    """Tax information for a specific period."""
    year: str
    label: str
    amount_paid: str
    balance_due: str
    amount_paid_decimal: float
    balance_due_decimal: float


class TaxSummaryResponse(BaseModel):
    """Response model for tax summary."""
    success: bool
    title: str
    stub_number: Optional[str]
    periods: List[TaxPeriod]
    total: TaxPeriod
    tax_year_code: str


# Helper function to convert Decimal to float for JSON serialization
def decimal_to_dict(data: Dict[str, object]) -> Dict:
    """Convert Decimal objects to floats for JSON serialization."""
    result = {}
    for key, value in data.items():
        if isinstance(value, Decimal):
            result[key] = float(value)
        elif isinstance(value, dict):
            result[key] = decimal_to_dict(value)
        elif isinstance(value, list):
            result[key] = [
                decimal_to_dict(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[key] = value
    return result


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Multi-County Property Search API",
        "version": "2.0.0",
        "counties": len(SUPPORTED_COUNTIES),
        "endpoints": {
            "counties": "GET /counties",
            "search": "POST /search/address",
            "map_search": "GET /search/map/{map_number}",
            "tax_summary": "GET /tax-summary",
        },
    }


@app.get("/counties")
async def get_counties():
    """Get list of supported counties."""
    return {
        "success": True,
        "count": len(SUPPORTED_COUNTIES),
        "counties": list(SUPPORTED_COUNTIES.values())
    }


@app.post("/search/address", response_model=SearchResponse)
async def search_address(request: AddressSearchRequest):
    """
    Search for properties by address.

    Supports multiple counties. Specify county in request body.
    Returns a list of matching properties with their details and tax information URLs.
    """
    if not request.street:
        raise HTTPException(status_code=400, detail="Street name is required")

    # Validate county
    if request.county not in SUPPORTED_COUNTIES:
        raise HTTPException(
            status_code=400,
            detail=f"County '{request.county}' not supported. Available: {list(SUPPORTED_COUNTIES.keys())}"
        )

    county_info = SUPPORTED_COUNTIES[request.county]

    # Check if county has search implemented
    if county_info.get("status") == "coming_soon":
        raise HTTPException(
            status_code=501,
            detail=f"{county_info['name']} search is coming soon"
        )

    session = requests.Session()

    try:
        # Route to appropriate county scraper
        if request.county == "fairfax-va":
            results, _ = search_fairfax_address(
                number=request.number,
                street=request.street.upper(),
                suffix=request.suffix.upper(),
                unit=request.unit,
                page_size=request.page_size,
                session=session,
            )
        else:
            raise HTTPException(
                status_code=501,
                detail=f"{county_info['name']} search not yet implemented"
            )

        return SearchResponse(
            success=True,
            count=len(results),
            results=results,
        )

    except requests.RequestException as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Search request failed: {str(exc)}"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during search: {str(exc)}"
        )


@app.get("/search/map/{map_number}")
async def search_by_map_number(map_number: str):
    """
    Search for a property by map number and return property details with tax information.

    This endpoint searches for a specific property using its Fairfax County map number
    (e.g., "0583 01 0001") and returns both the property details and tax summary in one call.
    """
    session = requests.Session()

    try:
        # Search by map number
        results, _ = search_fairfax_map_number(
            map_number=map_number,
            session=session,
        )

        if not results:
            raise HTTPException(
                status_code=404,
                detail=f"No property found with map number: {map_number}"
            )

        # Get the first result (should be exact match)
        property_data = results[0]
        detail_url = property_data.get("DetailURL")

        if not detail_url:
            return {
                "success": True,
                "property": property_data,
                "tax_summary": None,
                "message": "Property found but no detail URL available"
            }

        # Fetch tax summary
        try:
            tax_summary = fetch_fairfax_tax_summary(session, detail_url)

            # Convert tax summary for JSON
            periods = []
            for period in tax_summary.get("periods", []):
                periods.append({
                    "year": period["year"],
                    "label": period["label"],
                    "amount_paid": period["amount_paid_display"],
                    "balance_due": period["balance_due_display"],
                    "amount_paid_decimal": float(period["amount_paid"]),
                    "balance_due_decimal": float(period["balance_due"]),
                })

            total = tax_summary.get("total", {})
            total_data = {
                "year": total.get("year", "Total"),
                "label": total.get("label", ""),
                "amount_paid": total.get("amount_paid_display", "$0.00"),
                "balance_due": total.get("balance_due_display", "$0.00"),
                "amount_paid_decimal": float(total.get("amount_paid", 0)),
                "balance_due_decimal": float(total.get("balance_due", 0)),
            }

            return {
                "success": True,
                "property": property_data,
                "tax_summary": {
                    "title": tax_summary.get("title", "Tax Summary"),
                    "stub_number": tax_summary.get("stub_number"),
                    "tax_year_code": tax_summary.get("tax_year_code", ""),
                    "periods": periods,
                    "total": total_data,
                }
            }

        except (requests.RequestException, ValueError) as exc:
            # Return property data even if tax summary fails
            return {
                "success": True,
                "property": property_data,
                "tax_summary": None,
                "message": f"Property found but tax summary unavailable: {str(exc)}"
            }

    except requests.RequestException as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Search request failed: {str(exc)}"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during search: {str(exc)}"
        )


@app.get("/tax-summary", response_model=TaxSummaryResponse)
async def get_tax_summary(
    detail_url: str = Query(..., description="The DetailURL from search results")
):
    """
    Get tax summary for a specific property.

    Requires the DetailURL obtained from the address search endpoint.
    """
    if not detail_url:
        raise HTTPException(status_code=400, detail="detail_url parameter is required")

    # Decode the URL if it's encoded
    detail_url = unquote(detail_url)

    session = requests.Session()

    try:
        summary = fetch_fairfax_tax_summary(session, detail_url)

        # Convert the summary data for JSON serialization
        periods = []
        for period in summary.get("periods", []):
            periods.append(TaxPeriod(
                year=period["year"],
                label=period["label"],
                amount_paid=period["amount_paid_display"],
                balance_due=period["balance_due_display"],
                amount_paid_decimal=float(period["amount_paid"]),
                balance_due_decimal=float(period["balance_due"]),
            ))

        total = summary.get("total", {})
        total_period = TaxPeriod(
            year=total.get("year", "Total"),
            label=total.get("label", ""),
            amount_paid=total.get("amount_paid_display", "$0.00"),
            balance_due=total.get("balance_due_display", "$0.00"),
            amount_paid_decimal=float(total.get("amount_paid", 0)),
            balance_due_decimal=float(total.get("balance_due", 0)),
        )

        return TaxSummaryResponse(
            success=True,
            title=summary.get("title", "Tax Summary"),
            stub_number=summary.get("stub_number"),
            periods=periods,
            total=total_period,
            tax_year_code=summary.get("tax_year_code", ""),
        )

    except requests.RequestException as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch tax details: {str(exc)}"
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Failed to parse tax details: {str(exc)}"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(exc)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
