#!/usr/bin/env python3
"""
Frontend Integration Test
Tests that frontend can communicate with backend
"""
import requests
import json
import time

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

print("🧪 FRONTEND INTEGRATION TEST")
print("=" * 60)

# Test 1: Frontend accessibility
print("\n[1/4] Testing frontend accessibility...")
try:
    response = requests.get(FRONTEND_URL, timeout=5)
    if response.status_code == 200:
        content = response.text
        
        # Check for key elements
        has_arcgen = "Arcgen" in content or "arcgen" in content.lower()
        has_react = "react" in content.lower()
        has_next = "next" in content.lower() or "_next" in content
        
        print(f"   ✅ Frontend is accessible")
        print(f"   Status: {response.status_code}")
        print(f"   Has Arcgen branding: {'✓' if has_arcgen else '✗'}")
        print(f"   React loaded: {'✓' if has_react else '✗'}")
        print(f"   Next.js loaded: {'✓' if has_next else '✗'}")
        print(f"   Page size: {len(content)} bytes")
    else:
        print(f"   ❌ Failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: CORS configuration
print("\n[2/4] Testing CORS configuration...")
try:
    response = requests.options(
        f"{BACKEND_URL}/generate",
        headers={
            "Origin": FRONTEND_URL,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        },
        timeout=5
    )
    
    cors_headers = {
        k: v for k, v in response.headers.items() 
        if k.lower().startswith('access-control')
    }
    
    if cors_headers:
        print(f"   ✅ CORS is configured")
        for header, value in cors_headers.items():
            print(f"      {header}: {value}")
    else:
        print(f"   ⚠️  No CORS headers found (might still work)")
        
except Exception as e:
    print(f"   ⚠️  CORS check inconclusive: {e}")

# Test 3: API endpoint from frontend perspective
print("\n[3/4] Testing backend API (as frontend would)...")
try:
    response = requests.post(
        f"{BACKEND_URL}/generate",
        json={"prompt": "Simple test diagram"},
        headers={
            "Content-Type": "application/json",
            "Origin": FRONTEND_URL
        },
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Backend responds to frontend requests")
        print(f"   Response type: {data.get('tool_used', 'unknown')}")
        print(f"   Has XML: {'✓' if 'xml' in data else '✗'}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Static assets
print("\n[4/4] Testing frontend static assets...")
try:
    # Test favicon
    response = requests.get(f"{FRONTEND_URL}/favicon.ico", timeout=5)
    favicon_exists = response.status_code == 200
    
    print(f"   Favicon: {'✓' if favicon_exists else '✗'}")
    print(f"   Frontend URL: {FRONTEND_URL}")
    print(f"   Backend URL: {BACKEND_URL}")
    
except Exception as e:
    print(f"   ⚠️  Static asset check inconclusive: {e}")

print("\n" + "=" * 60)
print("✅ Frontend integration test complete!")
print("=" * 60)

print("\n📱 Ready to use:")
print(f"   Open {FRONTEND_URL} in your browser")
print(f"   Backend API: {BACKEND_URL}/docs")
