#!/usr/bin/env python3
"""
Test additional Arcgen features
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("🧪 TESTING ADDITIONAL FEATURES")
print("=" * 60)

# Test 1: Available providers
print("\n[1/6] Testing providers endpoint...")
try:
    response = requests.get(f"{BASE_URL}/providers", timeout=5)
    if response.status_code == 200:
        data = response.json()
        providers = data.get('providers', {})
        current = data.get('current_provider', 'unknown')
        print(f"   ✅ Success")
        print(f"   Available providers: {len(providers)}")
        print(f"   Current provider: {current}")
        print(f"   Providers: {', '.join(providers.keys())}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Model config
print("\n[2/6] Testing model config...")
try:
    response = requests.get(f"{BASE_URL}/llm-config", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Success")
        print(f"   Provider: {data.get('provider')}")
        print(f"   Model: {data.get('model')}")
        print(f"   API Key: {'✓' if data.get('api_key_configured') else '✗'}")
        print(f"   Base URL: {data.get('base_url')}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Shape libraries
print("\n[3/6] Testing shape libraries...")
try:
    response = requests.get(f"{BASE_URL}/shape-libraries", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Success")
        print(f"   Libraries available: {len(data.get('libraries', []))}")
        libs = data.get('libraries', [])[:5]
        print(f"   Sample libraries: {', '.join(libs)}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Upload file endpoint (without actual file)
print("\n[4/6] Testing upload endpoint availability...")
try:
    # Just check if endpoint exists (will fail without file, which is expected)
    response = requests.post(f"{BASE_URL}/upload-file", timeout=5)
    # We expect this to fail, but endpoint should exist
    if response.status_code == 422:  # Validation error (no file)
        print(f"   ✅ Endpoint exists (422 validation expected)")
    else:
        print(f"   ⚠️  Endpoint returned: {response.status_code}")
except Exception as e:
    if "422" in str(e):
        print(f"   ✅ Endpoint exists")
    else:
        print(f"   ❌ Error: {e}")

# Test 5: Health check with docs
print("\n[5/6] Testing API documentation...")
try:
    response = requests.get(f"{BASE_URL}/docs", timeout=5)
    if response.status_code == 200:
        print(f"   ✅ API docs available at {BASE_URL}/docs")
    else:
        print(f"   ❌ Failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 6: OpenAPI spec
print("\n[6/6] Testing OpenAPI specification...")
try:
    response = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ OpenAPI spec available")
        print(f"   API Title: {data.get('info', {}).get('title')}")
        print(f"   Version: {data.get('info', {}).get('version')}")
        print(f"   Endpoints: {len(data.get('paths', {}))}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ Feature testing complete!")
print("=" * 60)
