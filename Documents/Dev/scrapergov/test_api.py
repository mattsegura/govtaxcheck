"""
Simple test script to verify the API is working correctly.

Run this after starting the server to test all endpoints.

Usage:
    python test_api.py
"""

import requests
import json
import sys


def test_health():
    """Test the health endpoint."""
    print("Testing /health endpoint...")
    try:
        response = requests.get("http://localhost:8001/health")
        if response.status_code == 200:
            print("✅ Health check passed:", response.json())
            return True
        else:
            print("❌ Health check failed with status:", response.status_code)
            return False
    except Exception as e:
        print("❌ Error connecting to server:", str(e))
        print("   Make sure the server is running!")
        return False


def test_root():
    """Test the root endpoint."""
    print("\nTesting / endpoint...")
    try:
        response = requests.get("http://localhost:8001/")
        if response.status_code == 200:
            data = response.json()
            print("✅ Root endpoint working:")
            print(f"   Version: {data.get('version')}")
            print(f"   Message: {data.get('message')}")
            return True
        else:
            print("❌ Root endpoint failed with status:", response.status_code)
            return False
    except Exception as e:
        print("❌ Error:", str(e))
        return False


def test_address_search():
    """Test the address search endpoint."""
    print("\nTesting /search/address endpoint...")
    try:
        payload = {
            "street": "MAIN",
            "suffix": "ST",
            "number": "",
            "unit": "",
            "page_size": "5"
        }
        response = requests.post(
            "http://localhost:8001/search/address",
            json=payload
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Address search successful:")
            print(f"   Found {data.get('count', 0)} results")
            if data.get('results') and len(data['results']) > 0:
                first = data['results'][0]
                print(f"   First result: {first.get('Property Address', 'N/A')}")
                print(f"   Owner: {first.get('Owner', 'N/A')}")
            return True
        else:
            print("❌ Address search failed with status:", response.status_code)
            print("   Response:", response.text)
            return False
    except Exception as e:
        print("❌ Error:", str(e))
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("API Test Suite - Fairfax County Property Search API")
    print("=" * 60)
    print("\nMake sure the server is running on http://localhost:8001")
    print("Start it with: python -m uvicorn api:app --reload --port 8001")
    print("\n" + "=" * 60 + "\n")

    results = []

    # Run tests
    results.append(("Health Check", test_health()))
    results.append(("Root Endpoint", test_root()))
    results.append(("Address Search", test_address_search()))

    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! The API is working correctly.")
        print("\nNext steps:")
        print("  1. Open http://localhost:8001/docs in your browser")
        print("  2. Try the interactive API documentation")
        print("  3. Test more complex searches")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
