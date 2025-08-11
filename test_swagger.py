#!/usr/bin/env python3
"""
Test script to verify Swagger documentation is working correctly.
"""

import requests
import json

def test_swagger_ui():
    """Test that Swagger UI is accessible and endpoints are documented."""
    
    base_url = "http://localhost:8000"
    
    # Test OpenAPI schema endpoint
    try:
        response = requests.get(f"{base_url}/openapi.json")
        if response.status_code == 200:
            schema = response.json()
            print("✅ OpenAPI schema is accessible")
            print(f"   Title: {schema.get('info', {}).get('title')}")
            print(f"   Version: {schema.get('info', {}).get('version')}")
            print(f"   Endpoints: {len(schema.get('paths', {}))}")
        else:
            print("❌ OpenAPI schema not accessible")
    except Exception as e:
        print(f"❌ Error accessing OpenAPI schema: {e}")
    
    # Test Swagger UI endpoint
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ Swagger UI is accessible at /docs")
        else:
            print("❌ Swagger UI not accessible")
    except Exception as e:
        print(f"❌ Error accessing Swagger UI: {e}")
    
    # Test ReDoc endpoint
    try:
        response = requests.get(f"{base_url}/redoc")
        if response.status_code == 200:
            print("✅ ReDoc is accessible at /redoc")
        else:
            print("❌ ReDoc not accessible")
    except Exception as e:
        print(f"❌ Error accessing ReDoc: {e}")

if __name__ == "__main__":
    print("Testing Swagger documentation...")
    test_swagger_ui()
    print("\nTo test manually:")
    print("1. Start the server: uvicorn backend.main:app --reload")
    print("2. Visit http://localhost:8000/docs for Swagger UI")
    print("3. Visit http://localhost:8000/redoc for ReDoc")
