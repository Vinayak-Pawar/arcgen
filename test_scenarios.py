#!/usr/bin/env python3
"""
Test multiple diagram generation scenarios
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

test_scenarios = [
    {
        "name": "Simple Architecture",
        "prompt": "Create a diagram with a client, API server, and database"
    },
    {
        "name": "Microservices",
        "prompt": "Design a microservices architecture with API gateway, auth service, user service, and database"
    },
    {
        "name": "Cloud Architecture",
        "prompt": "AWS architecture with EC2, RDS, and S3"
    }
]

print("🧪 TESTING MULTIPLE SCENARIOS")
print("=" * 60)

results = []

for i, scenario in enumerate(test_scenarios, 1):
    print(f"\n[{i}/{len(test_scenarios)}] Testing: {scenario['name']}")
    print(f"   Prompt: {scenario['prompt'][:50]}...")
    
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{BASE_URL}/generate",
            json={"prompt": scenario['prompt']},
            timeout=90
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            has_xml = 'xml' in data and '<mxCell' in data['xml']
            
            result = {
                "scenario": scenario['name'],
                "status": "✅ PASS",
                "time": f"{elapsed:.1f}s",
                "xml_length": len(data.get('xml', '')),
                "has_cells": has_xml
            }
            
            print(f"   ✅ Success in {elapsed:.1f}s")
            print(f"   XML length: {len(data.get('xml', ''))} chars")
            print(f"   Has diagram cells: {'Yes' if has_xml else 'No'}")
            
        else:
            result = {
                "scenario": scenario['name'],
                "status": "❌ FAIL",
                "time": f"{elapsed:.1f}s",
                "error": response.status_code
            }
            print(f"   ❌ Failed with status {response.status_code}")
            
        results.append(result)
        
    except Exception as e:
        result = {
            "scenario": scenario['name'],
            "status": "❌ ERROR",
            "error": str(e)
        }
        print(f"   ❌ Error: {e}")
        results.append(result)
    
    # Small delay between tests
    if i < len(test_scenarios):
        print("   Waiting 2s before next test...")
        time.sleep(2)

# Summary
print("\n" + "=" * 60)
print("📊 TEST SUMMARY")
print("=" * 60)

passed = sum(1 for r in results if r['status'] == "✅ PASS")
failed = len(results) - passed

print(f"\nTotal Tests: {len(results)}")
print(f"✅ Passed: {passed}")
print(f"❌ Failed: {failed}")

print("\nDetailed Results:")
for r in results:
    print(f"\n  {r['scenario']}")
    print(f"    Status: {r['status']}")
    if 'time' in r:
        print(f"    Time: {r['time']}")
    if 'xml_length' in r:
        print(f"    XML Length: {r['xml_length']} chars")
    if 'has_cells' in r:
        print(f"    Has Cells: {'✓' if r['has_cells'] else '✗'}")
    if 'error' in r:
        print(f"    Error: {r['error']}")

if passed == len(results):
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 60)
else:
    print(f"\n⚠️  {failed} test(s) failed")

print("\n✅ Testing complete!")
