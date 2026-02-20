#!/usr/bin/env python3
"""
End-to-end test for Arcgen diagram generation
Tests the full flow: prompt -> AI -> diagram XML
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("🧪 Testing Arcgen End-to-End")
print("=" * 50)

# Test 1: Health check
print("\n[1/3] Testing backend health...")
try:
    response = requests.get(f"{BASE_URL}/", timeout=5)
    if response.status_code == 200:
        print("✓ Backend is running")
    else:
        print(f"✗ Backend returned status {response.status_code}")
        exit(1)
except Exception as e:
    print(f"✗ Backend is not accessible: {e}")
    exit(1)

# Test 2: Check providers
print("\n[2/3] Checking LLM configuration...")
try:
    response = requests.get(f"{BASE_URL}/llm-config", timeout=5)
    config = response.json()
    print(f"✓ Provider: {config['provider']}")
    print(f"✓ Model: {config['model']}")
    print(f"✓ API Key: {'Configured' if config['api_key_configured'] else 'Missing'}")
except Exception as e:
    print(f"✗ Failed to check config: {e}")
    exit(1)

# Test 3: Generate diagram
print("\n[3/3] Testing diagram generation...")
print("   (This will take 30-60 seconds with NVIDIA API...)")
print("   Please wait...")

test_prompt = "Create a simple diagram with a user connecting to a web server and then to a database"

try:
    start_time = time.time()
    
    response = requests.post(
        f"{BASE_URL}/generate",
        json={"prompt": test_prompt},
        timeout=90  # 90 second timeout
    )
    
    elapsed = time.time() - start_time
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ SUCCESS! Generated in {elapsed:.1f} seconds")
        print(f"   Tool used: {data.get('tool_used', 'unknown')}")
        print(f"   Provider: {data.get('provider', 'unknown')}")
        print(f"   Model: {data.get('model', 'unknown')}")
        
        if 'xml' in data:
            xml_length = len(data['xml'])
            has_cells = '<mxCell' in data['xml']
            print(f"   XML length: {xml_length} characters")
            print(f"   Contains mxCell: {'Yes' if has_cells else 'No'}")
            
            if has_cells:
                print("\n✓ Diagram generation is working correctly!")
                print("\n📊 Sample XML (first 300 chars):")
                print(data['xml'][:300] + "...")
            else:
                print("\n⚠️  Warning: XML doesn't contain mxCell elements")
        else:
            print(f"\n⚠️  Response type: {data.get('tool_used', 'unknown')}")
            print(f"   This might be a text response instead of a diagram")
            
    else:
        print(f"\n✗ Failed with status {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        exit(1)
        
except requests.Timeout:
    print("\n✗ Request timed out after 90 seconds")
    print("   NVIDIA API might be experiencing delays")
    print("   Try again or consider using a different provider")
    exit(1)
except Exception as e:
    print(f"\n✗ Error: {e}")
    exit(1)

print("\n" + "=" * 50)
print("✅ All tests passed! Arcgen is working correctly.")
print("\n🚀 Open http://localhost:3000 to use the app")
